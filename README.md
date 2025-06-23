# Workout Buddy

A simple Flask app to help users find local workout partners with similar goals.

## Setup

Install dependencies and run the server:

```bash
pip install -r requirements.txt
python app.py
```

## API

- `POST /users` - Create a user profile. Include fields such as `name`, `email`, `age`, `gender`, `goals`, `workout_types`, `lat`, `lon`, and optional matching preferences (`max_distance`, `gender_pref`, `age_range`).
- `GET /matches/<user_id>?distance=<km>` - Get nearby users that match the requesting user's goals and preferences.
- `POST /connect/<user_id>/<other_id>` - Send a connection request to another user.
- `GET /connections/<user_id>` - View pending connection requests for a user.

## Testing

Run tests with `pytest`:

```bash
pytest
```
