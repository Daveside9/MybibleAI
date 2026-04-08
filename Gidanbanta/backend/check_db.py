import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('matchhang.db')
cursor = conn.cursor()

# Check total matches
cursor.execute('SELECT COUNT(*) FROM matches')
total = cursor.fetchone()[0]
print(f'Total matches in database: {total}')

# Check matches for today and next few days
today = datetime.now().date()
for i in range(7):
    check_date = today + timedelta(days=i)
    date_str = check_date.strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM matches WHERE DATE(scheduled_at) = ?', (date_str,))
    count = cursor.fetchone()[0]
    print(f'{date_str}: {count} matches')

# Show all matches with their dates
print('\nAll matches:')
cursor.execute('SELECT id, home_team, away_team, scheduled_at, status FROM matches ORDER BY scheduled_at')
for row in cursor.fetchall():
    print(row)

conn.close()
