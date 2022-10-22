import pytest

def test_create_user(client):
    response = client.post('/api/v1/users',
                            json={
                                'name': 'test',
                                'last_name': 'Test',
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
        ({'last_name': 'test', 'mail': 'test@wp.pl', 'password': '12345678'}, 'name'),
        ({'name': 'test', 'mail': 'test@wp.pl', 'password': '12345678'}, 'last_name'),
        ({'name': 'test', 'last_name': 'Test', 'password': '12345678'}, 'mail'),
        ({'name': 'test', 'last_name': 'Test', 'mail': 'test@wp.pl'}, 'password')
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
                                'last_name': 'Test',
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
                                'last_name': 'Test',
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


def test_login_user_invalid_password(client, user):
    response = client.post('/api/v1/login',
                            json={
                                'mail': user['mail'],
                                'password': 'wrong_password'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'mail' not in response_data
    assert 'name' not in response_data
    assert 'last_name' not in response_data
    assert 'Invalid credentials' in response_data['message']


def test_login_user_invalid_mail(client, user):
    response = client.post('/api/v1/login',
                            json={
                                'mail': 'wrong_mail',
                                'password': user['password']
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'mail' not in response_data
    assert 'name' not in response_data
    assert 'last_name' not in response_data
    assert 'Invalid credentials' in response_data['message']


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
    assert 'mail' not in response_data
    assert 'name' not in response_data
    assert 'last_name' not in response_data
    assert 'Invalid credentials' in response_data['message']
    

@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'mail': 'test@wp.pl'}, 'password'),
        ({'password': '12345678'}, 'mail')
    ]
)
def test_login_user_missing_data(client, data, missing_field):
    response = client.post('/api/v1/login',
                            json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


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
    assert response_data['last_name'] == user['last_name']
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


def test_update_password(client, user, token):
    response = client.put('/api/v1/update/password',
			                headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json={
                                'current_password': user['password'],
                                'new_password': 'new_password'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert user['mail'] in response_data['data'].values()
    assert user['name'] in response_data['data'].values()
    assert user['last_name'] in response_data['data'].values()


def test_update_password_missing_token(client, user):
    response = client.put('/api/v1/update/password',
                            json={
                                'current_password': user['password'],
                                'new_password': 'new_password'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert user['mail'] not in response_data
    assert user['name'] not in response_data
    assert user['last_name'] not in response_data


def test_update_password_invalid_current_password(client, token):
    response = client.put('/api/v1/update/password',
			                headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json={
                                'current_password': 'wrong_password',
                                'new_password': 'new_password'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'mail' not in response_data
    assert 'name' not in response_data
    assert 'last_name' not in response_data
    assert 'Invalid credentials' in response_data['message']


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'current_password': '12345678'}, 'new_password'),
        ({'new_password': 'new_password'}, 'current_password')
    ]
)
def test_update_password_missing_data(client, token, data, missing_field):
    response = client.put('/api/v1/update/password',
			                headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'mail' not in response_data
    assert 'name' not in response_data
    assert 'last_name' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_update_user_data(client, token):
    response = client.put('/api/v1/update/data',
			                headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json={
                                'name': 'new_name',
                                'last_name': 'new_last_name',
                                'mail': 'new_mail@wp.pl'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert 'new_mail@wp.pl' in response_data['data'].values()
    assert 'new_name' in response_data['data'].values()
    assert 'new_last_name' in response_data['data'].values()


def test_update_user_data_missing_token(client):
    response = client.put('/api/v1/update/data',
                            json={
                                'name': 'new_name',
                                'last_name': 'new_last_name',
                                'mail': 'new_mail@wp.pl'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'new_mail@wp.pl' not in response_data
    assert 'new_name' not in response_data
    assert 'new_last_name' not in response_data


def test_update_user_data_already_used_mail(client, user, token):
    response = client.put('/api/v1/update/data',
			                headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json={
                                'name': user['name'],
                                'last_name': user['last_name'],
                                'mail': user['mail']
                            })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert user['mail'] not in response_data
    assert user['name'] not in response_data
    assert user['last_name'] not in response_data


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'name': 'new_name', 'last_name': 'new_last_name'}, 'mail'),
        ({'name': 'new_name', 'mail': 'new_mail@wp.pl'}, 'last_name'),
        ({'last_name': 'new_last_name', 'mail': 'new_mail@wp.pl'}, 'name')
    ]
)
def test_update_user_data_missing_data(client, user, token, data, missing_field):
    response = client.put('/api/v1/update/data',
			                headers={
                                'Authorization': f'Bearer {token}'
                            },
                            json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert 'new_mail@wp.pl' not in response_data
    assert 'new_name' not in response_data
    assert 'new_last_name' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_get_users(client, user):
    response = client.get('/api/v1/users')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 1
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_records': 1,
            'current_page': '/api/v1/users?page=1',
            'current_page (number)': 1,
        }

def test_get_users_no_records(client):
    response = client.get('/api/v1/users')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert len(response_data['data']) == 0
    assert response_data['pagination'] == {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/users?page=1',
            'current_page (number)': 1,
        }


def test_get_single_user(client, user):
    response = client.get('/api/v1/users/tesTes0')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['name'] == 'test'
    assert response_data['data']['last_name'] == 'Test'


def test_get_single_user_not_found(client, user):
    response = client.get('/api/v1/users/wrong_user_id')
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data