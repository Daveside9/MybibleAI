"""
Match Service
Business logic for match operations and API synchronization
"""
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.match import Match, Team, League, MatchStatus
from app.services.football_api import FootballAPIClient
from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)


class MatchService:
    """Service for match data synchronization and management"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_client = None
    
    async def _get_api_client(self) -> FootballAPIClient:
        """Get or create API client"""
        if not self.api_client:
            self.api_client = FootballAPIClient(
                api_key=settings.FOOTBALL_API_KEY,
                base_url=settings.FOOTBALL_API_BASE_URL,
                rapidapi_host=settings.RAPIDAPI_HOST
            )
        return self.api_client
    
    async def sync_matches(
        self, 
        date_from: str, 
        date_to: str,
        league_id: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Sync matches from Football API to database
        
        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            league_id: Optional league ID filter
        
        Returns:
            Dictionary with sync statistics
        """
        stats = {
            "fetched": 0,
            "created": 0,
            "updated": 0,
            "errors": 0
        }
        
        try:
            # Get API client
            async with await self._get_api_client() as client:
                # Fetch fixtures from API
                fixtures = await client.get_fixtures(
                    date_from=date_from,
                    date_to=date_to,
                    league_id=league_id
                )
                
                stats["fetched"] = len(fixtures)
                logger.info(f"Fetched {len(fixtures)} fixtures from API")
                
                # Process each fixture
                for fixture_data in fixtures:
                    try:
                        result = await self._process_fixture(fixture_data)
                        if result == "created":
                            stats["created"] += 1
                        elif result == "updated":
                            stats["updated"] += 1
                    except Exception as e:
                        logger.error(f"Error processing fixture: {e}")
                        stats["errors"] += 1
                
                # Invalidate cache after sync
                await cache_service.invalidate_all_matches()
                
                logger.info(f"Sync complete: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"Error syncing matches: {e}")
            stats["errors"] += 1
            return stats
    
    async def _process_fixture(self, fixture_data: Dict) -> str:
        """
        Process a single fixture from API
        
        Args:
            fixture_data: Fixture data from API
        
        Returns:
            "created" or "updated"
        """
        # Validate fixture data
        if not fixture_data.get("fixture") or not fixture_data.get("teams"):
            logger.warning("Invalid fixture data, skipping")
            return "error"
        
        fixture = fixture_data["fixture"]
        teams = fixture_data["teams"]
        league_data = fixture_data.get("league", {})
        
        external_id = fixture["id"]
        
        # Get or create teams
        home_team = await self._get_or_create_team(teams["home"])
        away_team = await self._get_or_create_team(teams["away"])
        
        # Get or create league
        league = await self._get_or_create_league(league_data)
        
        # Parse match time
        scheduled_time = datetime.fromisoformat(
            fixture["date"].replace("Z", "+00:00")
        )
        
        # Map API status to our status
        status = self._map_status(fixture["status"]["short"])
        
        # Check if match exists
        existing_match = self.db.query(Match).filter(
            Match.external_id == external_id
        ).first()
        
        if existing_match:
            # Update existing match
            existing_match.home_team_id = home_team.id
            existing_match.away_team_id = away_team.id
            existing_match.league_id = league.id
            existing_match.scheduled_at = scheduled_time
            existing_match.status = status
            existing_match.home_score = fixture.get("goals", {}).get("home") or 0
            existing_match.away_score = fixture.get("goals", {}).get("away") or 0
            existing_match.last_synced = datetime.utcnow()
            
            self.db.commit()
            return "updated"
        else:
            # Create new match
            new_match = Match(
                external_id=external_id,
                title=f"{teams['home']['name']} vs {teams['away']['name']}",
                home_team=teams["home"]["name"],
                away_team=teams["away"]["name"],
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league_id=league.id,
                scheduled_at=scheduled_time,
                status=status,
                home_score=fixture.get("goals", {}).get("home") or 0,
                away_score=fixture.get("goals", {}).get("away") or 0,
                home_odds=1.9,  # Default odds, will be updated separately
                away_odds=1.9,
                draw_odds=3.0,
                last_synced=datetime.utcnow()
            )
            
            self.db.add(new_match)
            self.db.commit()
            return "created"
    
    async def _get_or_create_team(self, team_data: Dict) -> Team:
        """Get or create team from API data"""
        external_id = team_data["id"]
        
        team = self.db.query(Team).filter(
            Team.external_id == external_id
        ).first()
        
        if not team:
            team = Team(
                external_id=external_id,
                name=team_data["name"],
                logo=team_data.get("logo")
            )
            self.db.add(team)
            self.db.commit()
            self.db.refresh(team)
        
        return team
    
    async def _get_or_create_league(self, league_data: Dict) -> League:
        """Get or create league from API data"""
        external_id = league_data["id"]
        
        league = self.db.query(League).filter(
            League.external_id == external_id
        ).first()
        
        if not league:
            league = League(
                external_id=external_id,
                name=league_data["name"],
                country=league_data.get("country", "Unknown"),
                logo=league_data.get("logo"),
                priority=self._get_league_priority(league_data["name"])
            )
            self.db.add(league)
            self.db.commit()
            self.db.refresh(league)
        
        return league
    
    def _map_status(self, api_status: str) -> MatchStatus:
        """Map API status to our MatchStatus enum"""
        status_map = {
            "TBD": MatchStatus.SCHEDULED,
            "NS": MatchStatus.SCHEDULED,
            "1H": MatchStatus.LIVE,
            "HT": MatchStatus.LIVE,
            "2H": MatchStatus.LIVE,
            "ET": MatchStatus.LIVE,
            "P": MatchStatus.LIVE,
            "FT": MatchStatus.FINISHED,
            "AET": MatchStatus.FINISHED,
            "PEN": MatchStatus.FINISHED,
            "PST": MatchStatus.POSTPONED,
            "CANC": MatchStatus.CANCELLED,
            "ABD": MatchStatus.CANCELLED,
            "AWD": MatchStatus.FINISHED,
            "WO": MatchStatus.FINISHED,
            "SUSP": MatchStatus.SUSPENDED
        }
        
        return status_map.get(api_status, MatchStatus.SCHEDULED)
    
    def _get_league_priority(self, league_name: str) -> int:
        """Assign priority to popular leagues"""
        priority_leagues = {
            "Premier League": 100,
            "La Liga": 95,
            "Serie A": 90,
            "Bundesliga": 85,
            "Ligue 1": 80,
            "UEFA Champions League": 110,
            "UEFA Europa League": 75,
            "World Cup": 120,
            "AFCON": 70
        }
        
        return priority_leagues.get(league_name, 0)
    
    async def update_live_matches(self) -> Dict[str, int]:
        """
        Update currently live matches
        
        Returns:
            Dictionary with update statistics
        """
        stats = {
            "fetched": 0,
            "updated": 0,
            "errors": 0
        }
        
        try:
            async with await self._get_api_client() as client:
                # Fetch live fixtures
                live_fixtures = await client.get_live_fixtures()
                
                stats["fetched"] = len(live_fixtures)
                logger.info(f"Fetched {len(live_fixtures)} live fixtures")
                
                # Update each live match
                for fixture_data in live_fixtures:
                    try:
                        await self._process_fixture(fixture_data)
                        stats["updated"] += 1
                    except Exception as e:
                        logger.error(f"Error updating live fixture: {e}")
                        stats["errors"] += 1
                
                # Invalidate live matches cache
                await cache_service.invalidate_all_matches()
                
                logger.info(f"Live update complete: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"Error updating live matches: {e}")
            stats["errors"] += 1
            return stats
    
    async def sync_next_14_days(self) -> Dict[str, int]:
        """
        Sync matches for the next 14 days
        
        Returns:
            Dictionary with sync statistics
        """
        today = datetime.now().date()
        end_date = today + timedelta(days=14)
        
        return await self.sync_matches(
            date_from=str(today),
            date_to=str(end_date)
        )


def get_match_service(db: Session) -> MatchService:
    """Dependency for match service"""
    return MatchService(db)
