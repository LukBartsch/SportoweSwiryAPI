import pytest

from SportoweSwiryAPI_app import create_app, db

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