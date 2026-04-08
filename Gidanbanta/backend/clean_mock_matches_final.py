#!/usr/bin/env python3
"""
Clean Mock Matches - Final Solution
Removes all test/mock matches by handling foreign key constraints properly
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_, text

def clean_mock_matches():
    """Clean all mock/test matches by handling relationships properly"""
    
    db = next(get_db())
    
    try:
        print('🧹 Starting comprehensive mock match cleanup...')
        
        # Find all mock matches
        mock_matches = db.query(Match).filter(
            or_(
                # Matches with suspicious external IDs (999xxx - clearly test data)
                Match.external_id.between(999000, 999999),
                
                # Matches with test/demo stream URLs
                Match.stream_url.like('%demo%'),
                Match.stream_url.like('%test%'),
                Match.stream_url.like('%bitdash%'),
                Match.stream_url.like('%tears-of-steel%'),
                Match.stream_url.like('%sintel%'),
                
                # Matches without external_id or with external_id = 0
                Match.external_id.is_(None),
                Match.external_id == 0
            )
        ).all()
        
        if not mock_matches:
            print('✅ No mock matches found - database is clean!')
            return
        
        mock_match_ids = [match.id for match in mock_matches]
        print(f'Found {len(mock_matches)} mock matches to clean')
        
        # Show sample of what will be deleted
        for i, match in enumerate(mock_matches[:3]):
            external_id = match.external_id or 'None'
            print(f'  {i+1}. ID: {match.id} | External: {external_id} | {match.home_team} vs {match.away_team}')
        
        if len(mock_matches) > 3:
            print(f'  ... and {len(mock_matches) - 3} more')
        
        # Count before cleanup
        total_before = db.query(Match).count()
        
        # Step 1: Delete match rooms using raw SQL to avoid constraint issues
        print('🗑️  Cleaning match rooms...')
        if mock_match_ids:
            placeholders = ','.join(['?' for _ in mock_match_ids])
            rooms_result = db.execute(
                text(f"DELETE FROM match_rooms WHERE match_id IN ({placeholders})"),
                mock_match_ids
            )
            print(f'   Removed {rooms_result.rowcount} match rooms')
        
        # Step 2: Delete transactions
        print('🗑️  Cleaning transactions...')
        if mock_match_ids:
            trans_result = db.execute(
                text(f"DELETE FROM transactions WHERE match_id IN ({placeholders})"),
                mock_match_ids
            )
            print(f'   Removed {trans_result.rowcount} transactions')
        
        # Step 3: Delete the matches themselves
        print('🗑️  Removing mock matches...')
        if mock_match_ids:
            match_result = db.execute(
                text(f"DELETE FROM matches WHERE id IN ({placeholders})"),
                mock_match_ids
            )
            print(f'   Removed {match_result.rowcount} matches')
        
        # Commit all changes
        db.commit()
        
        # Verify cleanup
        total_after = db.query(Match).count()
        real_matches = db.query(Match).filter(Match.external_id > 0).count()
        
        # Check for remaining mock matches
        remaining_mock = db.query(Match).filter(
            or_(
                Match.external_id.between(999000, 999999),
                Match.stream_url.like('%demo%'),
                Match.stream_url.like('%test%'),
                Matctches()lean_mock_ma   c_":
 __main_e__ == "
if __nam()
  db.closelly:
        fina raise
  )
       lback(b.rol)
        d}'{eup: uring cleanError drint(f'❌        p:
 on as et Excepti
    excep         main')
   rees still } mock matchning_mockng: {remainiar\\n⚠️  Wnt(f'       prilse:
          e')
   anedrly clehips propeionsatgn key relll forei  ✅ A' (fprint        n')
    remai URLs demo streamo test/int(f'   ✅ N pr           rnal IDs')
id extees with val matchly realntains onco✅ Database (f'   ntri        p')
    ly removed!ompletes cock matcheAll m SUCCESS: n🎉'\\   print(f    == 0:
     ck maining_mo reif               

 )ches}'al_matatches: {re real m   Remainingint(f'  pr     matches')
 fter} mock e - total_atal_befor: {tovedt(f'   Remo   prines')
     matchfter} total : {total_a(f'   After print       s')
otal matchee} ttotal_befor: { Beforent(f'  
        prieted!')p complch cleanu Mock matn✅print(f'\\        
 t()
         ).coun    )
           
   = 0id =l_tch.externa          Ma
      one),s_(Nnal_id.iatch.exter   M             dash%'),
like('%bit_url.h.stream