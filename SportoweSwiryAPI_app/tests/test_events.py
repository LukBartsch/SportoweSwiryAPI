import datetime as dt

def test_get_my_events(client, token, sample_event):
    response = client.get('/api/v1/events',
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
            'current_page': '/api/v1/events?page=1',
            'current_page (number)': 1
        }


def test_get_my_events_no_records(client, token):
    response = client.get('/api/v1/events',
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
            'current_page': '/api/v1/events?page=1',
            'current_page (number)': 1
        }
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_my_events_missing_token(client, token, sample_event):
    response = client.get('/api/v1/events')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'number_of_records' not in response_data
    assert 'pagination' not in response_data


def test_get_my_events_with_params(client, token, sample_event):
    response = client.get('/api/v1/events?fields=name,start,length_weeks,admin_id&sort=name&page=1&limit=1',
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
            'current_page': '/api/v1/events?page=1&fields=name,start,length_weeks,admin_id&sort=name&limit=1',
            'current_page (number)': 1
        }
    assert response_data['data'] == [
        {
            'admin_id': 'tesAdm0',
            'length_weeks': 10,
            'name': 'Event_Test2',
            'start': str(dt.date.today().strftime("%d-%m-%Y"))   
        }
    ]














def test_get_all_events(client, token, sample_event):
    response = client.get('/api/v1/all_events',
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
            'current_page': '/api/v1/all_events?page=1',
            'current_page (number)': 1
        }
        


def test_get_all_events_no_records(client, token):
    response = client.get('/api/v1/all_events',
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
            'current_page': '/api/v1/all_events?page=1',
            'current_page (number)': 1
        }
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_all_events_missing_token(client, token, sample_event):
    response = client.get('/api/v1/all_events')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'number_of_records' not in response_data
    assert 'pagination' not in response_data


def test_get_all_events_with_params(client, token, sample_event):
    response = client.get('/api/v1/all_events?fields=name,start,length_weeks,admin_id&sort=name&page=1&limit=2',
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
            'current_page': '/api/v1/all_events?page=1&fields=name,start,length_weeks,admin_id&sort=name&limit=2',
            'current_page (number)': 1
        }
    assert response_data['data'] == [
        {
            'admin_id': 'tesAdm0',
            'length_weeks': 5,
            'name': 'Event_Test1',
            'start': str(dt.date.today().strftime("%d-%m-%Y"))   
        },
        {
            'admin_id': 'tesAdm0',
            'length_weeks': 10,
            'name': 'Event_Test2',
            'start': str(dt.date.today().strftime("%d-%m-%Y"))   
        }
    ]


def test_get_available_events(client, token, sample_event):
    response = client.get('/api/v1/available_events',
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
            'current_page': '/api/v1/available_events?page=1',
            'current_page (number)': 1
        }


def test_get_available_events_no_records(client, token):
    response = client.get('/api/v1/available_events',
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
            'current_page': '/api/v1/available_events?page=1',
            'current_page (number)': 1
        }
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_available_events_missing_token(client, token, sample_event):
    response = client.get('/api/v1/available_events')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'number_of_records' not in response_data
    assert 'pagination' not in response_data


def test_get_available_events_with_params(client, token, sample_event):
    response = client.get('/api/v1/available_events?fields=name,start,length_weeks,admin_id&sort=name&page=1&limit=2',
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
            'current_page': '/api/v1/available_events?page=1&fields=name,start,length_weeks,admin_id&sort=name&limit=2',
            'current_page (number)': 1
        }
    assert response_data['data'] == [
        {
            'admin_id': 'tesAdm0',
            'length_weeks': 5,
            'name': 'Event_Test1',
            'start': str(dt.date.today().strftime("%d-%m-%Y"))   
        }
    ]