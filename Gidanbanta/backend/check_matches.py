import sqlite3
from datetime import datetime

conn = sqlite3.connect('matchhang.db')
cursor = conn.cursor()

cursor.execute('SELECT home_team, away_team, scheduled_at, status FROM matches ORDER BY scheduled_at')
matches = cursor.fetchall()

print('Matches in database:')
print('-' * 100)
for m in matches:
    print(f'{m[0]:20} vs {m[1]:20} | {m[2]} | Status: {m[3]}')

print(f'\nToday is: {datetime.now().date()}')
conn.close()
