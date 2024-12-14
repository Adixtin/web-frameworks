import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_full_user_lifecycle(client):
    create_response = client.post('/users', json={
        'name': 'Integration',
        'lastname': 'Tester'
    })
    assert create_response.status_code == 201

    get_all_response = client.get('/users')
    assert get_all_response.status_code == 200
    users = get_all_response.get_json()
    assert len(users) == 1
    assert users[0]['name'] == 'Integration'
    assert users[0]['lastname'] == 'Tester'

    get_response = client.get('/users/1')
    assert get_response.status_code == 200
    user = get_response.get_json()
    assert user['name'] == 'Integration'
    assert user['lastname'] == 'Tester'

    update_response = client.put('/users/1', json={
        'name': 'Updated',
        'lastname': 'User'
    })
    assert update_response.status_code == 204

    verify_update_response = client.get('/users/1')
    updated_user = verify_update_response.get_json()
    assert updated_user['name'] == 'Updated'
    assert updated_user['lastname'] == 'User'

    delete_response = client.delete('/users/1')
    assert delete_response.status_code == 204

    get_deleted_response = client.get('/users/1')
    assert get_deleted_response.status_code == 404

    final_users_response = client.get('/users')
    assert final_users_response.status_code == 200
    assert len(final_users_response.get_json()) == 0