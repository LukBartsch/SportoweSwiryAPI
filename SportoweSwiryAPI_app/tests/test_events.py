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
    assert response_data['message'] == 'Missing token. Please login to get new token'


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
    assert response_data['message'] == 'Missing token. Please login to get new token'


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
    assert response_data['message'] == 'Missing token. Please login to get new token'


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


def test_join_event(client, token, sample_event):
    response = client.get('/api/v1/join_event/1',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data'] == 'Congratulations. You signed up for event: Event_Test1'


def test_join_event_not_found(client, token, sample_event):
    response = client.get('/api/v1/join_event/99',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Event with id 99 not found'


def test_join_event_missing_token(client, token, sample_event):
    response = client.get('/api/v1/join_event/1')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert response_data['message'] == 'Missing token. Please login to get new token'


def test_join_event_current_unavailable(client, token, sample_event):
    response = client.get('/api/v1/join_event/2',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 403
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'Joining for this event (Event_Test2) is currently unavailable.'


def test_join_event_already_signed_up(client, token, sample_event):
    test_join_event(client, token, sample_event)
    response = client.get('/api/v1/join_event/1',
                            headers={
                                'Authorization': f'Bearer {token}'
                            })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert response_data['message'] == 'You are already signed up for this event (Event_Test1).'

