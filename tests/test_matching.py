import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import app, users, connections


def setup_function(_):
    users.clear()
    connections.clear()


def test_basic_match():
    with app.test_client() as client:
        client.post('/users', json={
            'name': 'Alice',
            'email': 'a@example.com',
            'age': 25,
            'gender': 'female',
            'goals': ['strength'],
            'lat': 0,
            'lon': 0
        })
        client.post('/users', json={
            'name': 'Bob',
            'email': 'b@example.com',
            'age': 26,
            'gender': 'male',
            'goals': ['strength'],
            'lat': 0,
            'lon': 0.05
        })
        resp = client.get('/matches/1?distance=10')
        matches = resp.get_json()
        assert len(matches) == 1
        assert matches[0]['name'] == 'Bob'


def test_gender_preference_blocks_match():
    with app.test_client() as client:
        client.post('/users', json={
            'name': 'Alice',
            'email': 'a@example.com',
            'gender': 'female',
            'goals': ['yoga'],
            'gender_pref': 'female',
            'lat': 0,
            'lon': 0
        })
        client.post('/users', json={
            'name': 'Bob',
            'email': 'b@example.com',
            'gender': 'male',
            'goals': ['yoga'],
            'lat': 0,
            'lon': 0
        })
        resp = client.get('/matches/1?distance=5')
        matches = resp.get_json()
        assert matches == []
