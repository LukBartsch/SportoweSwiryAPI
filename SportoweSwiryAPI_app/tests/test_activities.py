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


# def test_get_activities_with_params(client, token, sample_activity):
#     response = client.get('/api/v1/activities?fields=distance,time',
#                             headers={
#                                 'Authorization': f'Bearer {token}'
#                             })
#     response_data = response.get_json()
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#     assert response_data['success'] is True
#     assert response_data['number_of_records'] == 1
#     assert len(response_data['data']) == 1
#     assert response_data['pagination'] == {
#             'total_pages': 1,
#             'total_records': 1,
#             'current_page': '/api/v1/activities?fields=distance&sort=-user_id&page=1&limit=1',
#             'current_page (number)': 1,
#         }
#     assert response_data['data'] == [
#         {
#             'distance': 10
#         }
#     ]