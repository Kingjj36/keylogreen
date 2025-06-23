from flask import Flask, request, jsonify
from geopy.distance import geodesic

app = Flask(__name__)

# Simple in-memory storage for user profiles
users = {}

# simple in-memory store for pending connections
connections = {}

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    user_id = len(users) + 1
    profile = {
        'id': user_id,
        'name': data.get('name'),
        'email': data.get('email'),
        'age': data.get('age'),
        'gender': data.get('gender'),
        'goals': data.get('goals', []),
        'workout_types': data.get('workout_types', []),
        'location': {
            'lat': data.get('lat'),
            'lon': data.get('lon')
        },
        'max_distance': data.get('max_distance', 10),
        'gender_pref': data.get('gender_pref'),
        'age_range': data.get('age_range'),  # [min, max]
    }
    users[user_id] = profile
    connections[user_id] = []
    return jsonify(profile), 201


def distance_km(loc1, loc2):
    """Calculate geodesic distance in kilometers between two (lat, lon) pairs."""
    return geodesic(loc1, loc2).km


def _within_prefs(user, other):
    """Check gender and age preferences."""
    if user.get('gender_pref') and other.get('gender'):
        prefs = user['gender_pref']
        if isinstance(prefs, str):
            prefs = [prefs]
        if prefs and other['gender'] not in prefs:
            return False

    if user.get('age_range') and other.get('age'):
        min_age, max_age = user['age_range']
        if not (min_age <= other['age'] <= max_age):
            return False
    return True


def matches_for_user(user, max_distance):
    results = []
    for uid, other in users.items():
        if uid == user['id']:
            continue
        if not _within_prefs(user, other):
            continue
        if set(user.get('goals', [])) & set(other.get('goals', [])):
            d = distance_km(
                (user['location']['lat'], user['location']['lon']),
                (other['location']['lat'], other['location']['lon'])
            )
            if d <= max_distance and d <= other.get('max_distance', max_distance):
                results.append({'id': uid, 'name': other['name'], 'distance_km': d})
    return results


@app.route('/connect/<int:user_id>/<int:other_id>', methods=['POST'])
def send_connection(user_id, other_id):
    if user_id not in users or other_id not in users:
        return jsonify({'error': 'User not found'}), 404
    connections.setdefault(other_id, []).append(user_id)
    return jsonify({'status': 'pending'}), 201


@app.route('/connections/<int:user_id>')
def get_connections(user_id):
    pending = connections.get(user_id, [])
    return jsonify({'requests': pending})

@app.route('/matches/<int:user_id>')
def get_matches(user_id):
    max_distance = float(request.args.get('distance', 10))
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    matches = matches_for_user(user, max_distance)
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True)
