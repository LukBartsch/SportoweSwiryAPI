import pytest
import datetime as dt

from SportoweSwiryAPI_app import create_app, db
from SportoweSwiryAPI_app.models import Activities, Sport

@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    app.config['DB_FILE_PATH'].unlink(missing_ok=True)


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def user(client):
    user = {
        'name': 'test',
        'last_name': 'Test',
        'mail': 'test@wp.pl',
        'password': '12345678'
    }
    client.post('/api/v1/users', json=user)
    return user


@pytest.fixture
def token(client, user):
    response = client.post('/api/v1/login', json={
        'mail': user['mail'],
        'password': user['password']
    })
    return response.get_json()['token']


@pytest.fixture
def sample_activity(client):
    activity = {
        "user_id": "tesTes0",
        "activity_type_id": 3,
        "date": dt.date.today(),
        "distance": 8,
        "time": 1410,
    }
    sport = {
        "id": 3,
        "name": "Bieg",
        "default_coefficient": 1,
        "default_is_constant": False,
        "category": "other"
    }
    sample_activity = Activities(**activity)
    db.session.add(sample_activity)
    sample_sport = Sport(**sport)
    db.session.add(sample_sport)
    db.session.commit()
