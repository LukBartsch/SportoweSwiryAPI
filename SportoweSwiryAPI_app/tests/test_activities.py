import pytest
from datetime import datetime


def test_get_activities_no_records(client, token):
    response = client.get('/api/v1/activities',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/activities?page=1',
            'current_page (number)': 1
        }
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_activities(client, token, sample_activity):
    response = client.get('/api/v1/activities',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 2
    assert len(response_data['data']) == 2
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_records': 2,
            'current_page': '/api/v1/activities?page=1',
            'current_page (number)': 1
        }


def test_get_activities_missing_token(client, token, sample_activity):
    response = client.get('/api/v1/activities')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'number_of_records' not in response_data
    assert 'pagination' not in response_data


def test_get_activities_with_params(client, token, sample_activity):
    response = client.get('/api/v1/activities?fields=activity_type_id,activity_name,distance&sort=time&page=2&limit=1',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 1
    assert len(response_data['data']) == 1
    assert response_data['pagination'] == {
            'total_pages': 2,
            'total_records': 2,
            'current_page': '/api/v1/activities?page=2&fields=activity_type_id,activity_name,distance&sort=time&limit=1',
            'current_page (number)': 2,
            'previous_page': '/api/v1/activities?page=1&fields=activity_type_id,activity_name,distance&sort=time&limit=1'
        }
    assert response_data['data'] == [
        {
            'activity_name': 'Bieg',
            'activity_type_id': 3,
            'distance': '10.0'
        }
    ]


def test_get_types_of_activities(client, token, sample_activity):
    response = client.get('/api/v1/activities/types',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 1
    assert len(response_data['data']) == 1
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_records': 1,
            'current_page': '/api/v1/activities/types?page=1',
            'current_page (number)': 1,
        }


def test_get_types_of_activities_with_params(client, token, sample_activity):
    response = client.get('/api/v1/activities/types?fields=name,default_coefficient,default_is_constant',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 1
    assert len(response_data['data']) == 1
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_records': 1,
            'current_page': '/api/v1/activities/types?page=1&fields=name,default_coefficient,default_is_constant',
            'current_page (number)': 1,
        }
    assert response_data['data'] == [
        {
            'name': 'Bieg',
            'default_coefficient': '1.0',
            'default_is_constant': False
        }
    ]


def test_get_types_of_activities_no_records(client, token):
    response = client.get('/api/v1/activities/types',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    expected_result = {
        'success': True,
        'data': [],
        'number_of_records': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/activities/types?page=1',
            'current_page (number)': 1
        }
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_types_of_activities_missing_token(client, token, sample_activity):
    response = client.get('/api/v1/activities/types')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'number_of_records' not in response_data
    assert 'pagination' not in response_data


def test_add_activity(client, token, sample_activity):
    response = client.post('/api/v1/activities',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert 'Bieg' in response_data['data'].values()
    assert 3 in response_data['data'].values()
    assert '22-10-2022' in response_data['data'].values()
    assert '5.0' in response_data['data'].values()
    assert '0:30:00' in response_data['data'].values()


def test_add_activity_missing_token(client, token, sample_activity):
    response = client.post('/api/v1/activities',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Missing token. Please login to get new token'


def test_add_activity_invalid_conent_type(client, token, sample_activity):
    response = client.post('/api/v1/activities',
                            data={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Content type must be application/json'


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'activity_name': 'Bieg', 'date': '22-10-2022'}, 'distance'),
        ({'activity_name': 'Bieg', 'distance': '5'}, 'date'),
        ({'distance': '5', 'date': '22-10-2022'}, 'activity_name')
    ]
)
def test_add_activity_missing_data(client, token, data, missing_field):
    response = client.post('/api/v1/activities',
                            json=data,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_add_activity_invalid_sport_name(client, token, sample_activity):
    response = client.post('/api/v1/activities',
                            json={
                                'activity_name': 'Wrong_name',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['activity_name'] == ['This type of activity (Wrong_name) is not available in the application.']


def test_add_activity_invalid_date(client, token, sample_activity):
    response = client.post('/api/v1/activities',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2122',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['date'] == [f'Birth date must be lower than {datetime.now().date()}']


def test_add_activity_invalid_distance(client, token, sample_activity):
    response = client.post('/api/v1/activities',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': 'five',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['distance'] == ['Not a valid number.']


def test_update_activity(client, token, sample_activity):
    response = client.put('/api/v1/activities/1',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert 'Bieg' in response_data['data'].values()
    assert 3 in response_data['data'].values()
    assert '22-10-2022' in response_data['data'].values()
    assert '5.0' in response_data['data'].values()
    assert '0:30:00' in response_data['data'].values()


def test_update_activity_not_found(client, token, sample_activity):
    response = client.put('/api/v1/activities/99',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert response_data['message'] == 'Activity with id 99 not found'


def test_update_activity_missing_token(client, token, sample_activity):
    response = client.put('/api/v1/activities/1',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Missing token. Please login to get new token'


def test_update_activity_invalid_conent_type(client, token, sample_activity):
    response = client.put('/api/v1/activities/1',
                            data={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Content type must be application/json'


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'activity_name': 'Bieg', 'date': '22-10-2022'}, 'distance'),
        ({'activity_name': 'Bieg', 'distance': '5'}, 'date'),
        ({'distance': '5', 'date': '22-10-2022'}, 'activity_name')
    ]
)
def test_update_activity_missing_data(client, token, data, missing_field):
    response = client.put('/api/v1/activities/1',
                            json=data,
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]


def test_update_activity_invalid_sport_name(client, token, sample_activity):
    response = client.put('/api/v1/activities/1',
                            json={
                                'activity_name': 'Wrong_name',
                                'date': '22-10-2022',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['activity_name'] == ['This type of activity (Wrong_name) is not available in the application.']


def test_update_activity_invalid_date(client, token, sample_activity):
    response = client.put('/api/v1/activities/1',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2122',
                                'distance': '5',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['date'] == [f'Birth date must be lower than {datetime.now().date()}']


def test_update_activity_invalid_distance(client, token, sample_activity):
    response = client.put('/api/v1/activities/1',
                            json={
                                'activity_name': 'Bieg',
                                'date': '22-10-2022',
                                'distance': 'five',
                                'time': '0:30:00'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['distance'] == ['Not a valid number.']


def test_delete_activity(client, token, sample_activity):
    response = client.delete('/api/v1/activities/1',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == 'Activity with id 1 has been deleted'


def test_delete_activity_missing_token(client, token, sample_activity):
    response = client.delete('/api/v1/activities/1')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Missing token. Please login to get new token'


def test_delete_activity_not_found(client, token, sample_activity):
    response = client.delete('/api/v1/activities/99',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert response_data['message'] == 'Activity with id 99 not found'


def test_get_user_activities(client, token, sample_activity):
    response = client.post('/api/v1/user_activities',
                            json={
                                'id': 'tesTes0'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 2
    assert len(response_data['data']) == 2
    assert response_data['pagination'] == {
            'total_pages': 1,
            'total_records': 2,
            'current_page': '/api/v1/user_activities?page=1',
            'current_page (number)': 1
        }


def test_get_user_activities_missing_token(client, token, sample_activity):
    response = client.post('/api/v1/user_activities',
                            json={
                                'id': 'tesTes0'
                            })
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Missing token. Please login to get new token'


def test_get_user_activities_invalid_content_type(client, token, sample_activity):
    response = client.post('/api/v1/user_activities',
                            data={
                                'id': 'tesTes0'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Content type must be application/json'


def test_get_user_activities_not_found(client, token, sample_activity):
    response = client.post('/api/v1/user_activities',
                            json={
                                'id': 'wrong_id'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert response_data['message'] == 'User with id (username): wrong_id not found'


def test_get_user_activities_missing_id(client, token, sample_activity):
    response = client.post('/api/v1/user_activities',
                            json={},
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'id' in response_data['message']
    assert 'Missing data for required field.' in response_data['message']['id']


def test_get_user_activities_invalid_id(client, token, sample_activity):
    response = client.post('/api/v1/user_activities',
                            json={
                                'id': 123
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message']['id'] == ['Not a valid string.']


def test_get_user_activities_with_params(client, token, sample_activity):
    response = client.post('/api/v1/user_activities?fields=activity_type_id,activity_name,distance&sort=time&page=2&limit=1',
                            json={
                                'id': 'tesTes0'
                            },
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['number_of_records'] == 1
    assert len(response_data['data']) == 1
    assert response_data['pagination'] == {
            'total_pages': 2,
            'total_records': 2,
            'current_page': '/api/v1/user_activities?page=2&fields=activity_type_id,activity_name,distance&sort=time&limit=1',
            'current_page (number)': 2,
            'previous_page': '/api/v1/user_activities?page=1&fields=activity_type_id,activity_name,distance&sort=time&limit=1'
        }
    assert response_data['data'] == [
        {
            'activity_name': 'Bieg',
            'activity_type_id': 3,
            'distance': '10.0'
        }
    ]
