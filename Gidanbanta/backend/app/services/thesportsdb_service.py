"""
TheSportsDB Match Service
Business logic for syncing matches from TheSportsDB
"""
import logging
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.match import Match, Team, League, MatchStatus
from app.services.thesportsdb_api import TheSportsDBClient, THESPORTSDB_LEAGUES
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)


class TheSportsDBService:
    """Service for TheSportsDB match data synchronization"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_client = None
    
    async def _get_api_client(self) -> TheSportsDBClient:
        """Get or create API client"""
        if not self.api_client:
            self.api_client = TheSportsDBClient()
        return self.api_client
    
    async def sync_all_leagues(self) -> Dict[str, int]:
        """
        Sync matches from all major leagues
        
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
            async with await self._get_api_client() as client:
                
                for league_name, league_id in THESPORTSDB_LEAGUES.items():
                    logger.info(f"Syncing {league_name} (ID: {league_id})")
                    
                    try:
                        league_stats = await self._sync_league(client, league_name, league_id)
                        
                        # Add to totals
                        for key in stats:
                            stats[key] += league_stats.get(key, 0)
                        
                        # Small delay between leagues
                        await asyncio.sleep(1)
                        
                    except Exception as e:
                        logger.error(f"Error syncing {league_name}: {e}")
                        stats["errors"] += 1
                
                # Invalidate cache after sync
                await cache_service.invalidate_all_matches()
                
                logger.info(f"Total sync complete: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"Error syncing leagues: {e}")
            stats["errors"] += 1
            return stats
    
    async def _sync_league(
        self, 
        client: TheSportsDBClient, 
        league_name: str, 
        league_id: str
    ) -> Dict[str, int]:
        """
        Sync matches for a specific league
        
        Args:
            client: TheSportsDB API client
            league_name: Name of the league
            league_id: TheSportsDB league ID
        
        Returns:
            Dictionary with sync statistics for this league
        """
        stats = {
            "fetched": 0,
            "created": 0,
            "updated": 0,
            "errors": 0
        }
        
        try:
            # Get or create league
            league = await self._get_or_create_league(league_name, league_id)
            
            # Get next fixtures (upcoming matches)
            next_fixtures = await client.get_next_fixtures(league_id, count=20)
            
            # Get recent fixtures (for completed matches)
            past_fixtures = await client.get_last_fixtures(league_id, count=10)
            
            # Combine fixtures
            all_fixtures = next_fixtures + past_fixtures
            stats["fetched"] = len(all_fixtures)
            
            # Process each fixture
            for fixture_data in all_fixtures:
                try:
                    result = await self._process_fixture(fixture_data, league)
                    if result == "created":
                        stats["created"] += 1
                    elif result == "updated":
                        stats["updated"] += 1
                except Exception as e:
                    logger.error(f"Error processing fixture: {e}")
                    stats["errors"] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Error syncing league {league_name}: {e}")
            stats["errors"] += 1
            return stats
    
    async def _process_fixture(self, fixture_data: Dict, league: League) -> str:
        """
        Process a single fixture from TheSportsDB
        
        Args:
            fixture_data: Fixture data from API
            league: League object
        
        Returns:
            "created" or "updated"
        """
        # Validate fixture data
        if not fixture_data.get("idEvent"):
            logger.warning("Invalid fixture data, skipping")
            return "error"
        
        external_id = int(fixture_data["idEvent"])
        
        # Get team names
        home_team_name = fixture_data.get("strHomeTeam", "Unknown")
        away_team_name = fixture_data.get("strAwayTeam", "Unknown")
        
        # Get or create teams
        home_team = await self._get_or_create_team(home_team_name, fixture_data.get("idHomeTeam"))
        away_team = await self._get_or_create_team(away_team_name, fixture_data.get("idAwayTeam"))
        
        # Parse match time
        scheduled_time = self._parse_match_time(fixture_data)
        
        # Map status
        status = self._map_status(fixture_data)
        
        # Get scores
        home_score = self._parse_score(fixture_data.get("intHomeScore"))
        away_score = self._parse_score(fixture_data.get("intAwayScore"))
        
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
            existing_match.home_score = home_score
            existing_match.away_score = away_score
            existing_match.last_synced = datetime.utcnow()
            
            self.db.commit()
            return "updated"
        else:
            # Create new match
            new_match = Match(
                external_id=external_id,
                title=f"{home_team_name} vs {away_team_name}",
                home_team=home_team_name,
                away_team=away_team_name,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league_id=league.id,
                scheduled_at=scheduled_time,
                status=status,
                home_score=home_score,
                away_score=away_score,
                home_odds=1.9,  # Default odds
                away_odds=1.9,
                draw_odds=3.0,
                is_featured=league.priority > 80,  # Feature high-priority leagues
                last_synced=datetime.utcnow()
            )
            
            self.db.add(new_match)
            self.db.commit()
            return "created"
    
    async def _get_or_create_team(self, team_name: str, external_id: str = None) -> Team:
        """Get or create team from API data"""
        # Try to find by name first
        team = self.db.query(Team).filter(Team.name == team_name).first()
        
        if not team:
            team = Team(
                external_id=int(external_id) if external_id else None,
                name=team_name
            )
            self.db.add(team)
            self.db.commit()
            self.db.refresh(team)
        
        return team
    
    async def _get_or_create_league(self, league_name: str, external_id: str) -> League:
        """Get or create league from API data"""
        league = self.db.query(League).filter(League.name == league_name).first()
        
        if not league:
            # Map league to country and priority
            league_info = self._get_league_info(league_name)
            
            league = League(
                external_id=int(external_id),
                name=league_name,
                country=league_info["country"],
                priority=league_info["priority"]
            )
            self.db.add(league)
            self.db.commit()
            self.db.refresh(league)
        
        return league
    
    def _parse_match_time(self, fixture_data: Dict) -> datetime:
        """Parse match time from TheSportsDB format"""
        date_str = fixture_data.get("dateEvent")
        time_str = fixture_data.get("strTime")
        
        if not date_str:
            # Default to tomorrow if no date
            return datetime.now() + timedelta(days=1)
        
        try:
            # Parse date (format: YYYY-MM-DD)
            match_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Add time if available (format: HH:MM:SS)
            if time_str:
                try:
                    time_parts = time_str.split(":")
                    hour = int(time_parts[0])
                    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                    
                    match_date = match_date.replace(hour=hour, minute=minute)
                except:
                    # Default to 15:00 if time parsing fails
                    match_date = match_date.replace(hour=15, minute=0)
            else:
                # Default to 15:00 if no time provided
                match_date = match_date.replace(hour=15, minute=0)
            
            return match_date
            
        except Exception as e:
            logger.warning(f"Error parsing match time: {e}")
            return datetime.now() + timedelta(days=1)
    
    def _map_status(self, fixture_data: Dict) -> MatchStatus:
        """Map TheSportsDB status to our MatchStatus enum"""
        # TheSportsDB doesn't have detailed status, so we infer from scores and date
        home_score = fixture_data.get("intHomeScore")
        away_score = fixture_data.get("intAwayScore")
        
        # If both scores exist and are not null, match is finished
        if home_score is not None and away_score is not None:
            return MatchStatus.FINISHED
        
        # Check if match date is in the past (likely finished but no scores yet)
        date_str = fixture_data.get("dateEvent")
        if date_str:
            try:
                match_date = datetime.strptime(date_str, "%Y-%m-%d")
                if match_date.date() < datetime.now().date():
                    return MatchStatus.FINISHED
                elif match_date.date() == datetime.now().date():
                    # Could be live or scheduled today
                    return MatchStatus.SCHEDULED
            except:
                pass
        
        return MatchStatus.SCHEDULED
    
    def _parse_score(self, score_str: str) -> Optional[int]:
        """Parse score from string"""
        if score_str is None or score_str == "":
            return None
        
        try:
            return int(score_str)
        except:
            return None
    
    def _get_league_info(self, league_name: str) -> Dict[str, any]:
        """Get league country and priority"""
        league_map = {
            "Premier League": {"country": "England", "priority": 100},
            "La Liga": {"country": "Spain", "priority": 95},
            "Serie A": {"country": "Italy", "priority": 90},
            "Bundesliga": {"country": "Germany", "priority": 85},
            "Ligue 1": {"country": "France", "priority": 80},
            "Champions League": {"country": "Europe", "priority": 110},
            "Europa League": {"country": "Europe", "priority": 75}
        }
        
        return league_map.get(league_name, {"country": "Unknown", "priority": 50})


def get_thesportsdb_service(db: Session) -> TheSportsDBService:
    """Dependency for TheSportsDB service"""
    return TheSportsDBService(db)