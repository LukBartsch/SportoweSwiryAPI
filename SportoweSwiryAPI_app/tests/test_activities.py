import pytest


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
