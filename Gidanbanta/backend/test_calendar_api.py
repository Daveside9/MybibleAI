import requests
import json

# First login to get token
login_response = requests.post(
    'http://localhost:8000/api/v1/auth/login',
    json={
        'email': 'admin@matchhang.com',
        'password': 'admin123'
    }
)

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f'✓ Login successful, token: {token[:50]}...')
    
    # Test calendar endpoint
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test for Dec 4, 2025
    response = requests.get(
        'http://localhost:8000/api/v1/matches/calendar/matches',
        params={
            'start_date': '2025-12-04',
            'end_date': '2025-12-04'
        },
        headers=headers
    )
    
    print(f'\nCalendar API Response Status: {response.status_code}')
    print(f'Response Headers: {dict(response.headers)}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'\nResponse Data:')
        print(json.dumps(data, indent=2))
    else:
        print(f'Error: {response.text}')
else:
    print(f'Login failed: {login_response.status_code}')
    print(login_response.text)
