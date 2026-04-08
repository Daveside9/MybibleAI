#!/usr/bin/env python3
"""
Check Mock Matches - Identify what mock matches exist
"""

from app.core.database import get_db
from app.models.match import Match
from sqlalchemy import or_

def check_mock_matches():
    """Check what mock matches exist in the database"""
    
    db = next(get_db())
    
    try:
        print('🔍 Checking for mock matches in database...')
        
        # Find all mock matches based on multiple criteria
     