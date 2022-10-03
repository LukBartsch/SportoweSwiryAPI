import pytest

def test_create_user(client):
    response = client.post('/api/v1/users',
                            json={
                                'name': 'test',
                                'lastName': 'Test',
                                'mail': 'test@wp.pl',
                                'password': '12345678'
                            })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']

@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'lastName': 'test', 'mail': 'test@wp.pl', 'password': '12345678'}, 'name'),
        ({'name': 'test', 'mail': 'test@wp.pl', 'password': '12345678'}, 'lastName'),
        ({'name': 'test', 'lastName': 'Test', 'password': '12345678'}, 'mail'),
        ({'name': 'test', 'lastName': 'Test', 'mail': 'test@wp.pl'}, 'password')
    ]
)
def test_create_user_invalid_data(client, data, missing_field):
    response = client.post('/api/v1/users',
                            json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_create_user_invalid_content_type(client):
    response = client.post('/api/v1/users',
                            data={
                                'name': 'test',
                                'lastName': 'Test',
                                'mail': 'test@wp.pl',
                                'password': '12345678'
                            })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_create_user_already_used_mail(client, user):
    response = client.post('/api/v1/users',
                            json={
                                'name': 'test',
                                'lastName': 'Test',
                                'mail': user['mail'],
                                'password': '12345678'
                            })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_login_user(client, user):
    response = client.post('/api/v1/login',
                            json={
                                'mail': user['mail'],
                                'password': user['password']
                            })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert 'token' in response_data


def test_login_user_invalid_credentials(client):
    response = client.post('/api/v1/login',
                            json={
                                'mail': 'wrong_mail',
                                'password': 'wrong_password'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'Invalid credentials' in response_data['message']


def test_get_current_user(client, user, token):
    response = client.get('/api/v1/me',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['name'] == user['name']
    assert response_data['last_name'] == user['lastName']
    assert response_data['mail'] == user['mail']


def test_get_current_user_missing_token(client):
    response = client.get('/api/v1/me')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'name' not in response_data
    assert 'last_name' not in response_data
    assert 'mail' not in response_data