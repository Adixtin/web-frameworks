from app.app import app

def test_create_user_validation():

    with app.test_client() as client:
        response = client.post('/users', json={
            'lastname': 'Doe'
        })
        assert response.status_code == 400

        response = client.post('/users', json={
            'name': 'John'
        })
        assert response.status_code == 400

        response = client.post('/users', json={})
        assert response.status_code == 400

        response = client.post('/users', json={
            'name': 'Valid',
            'lastname': 'User'
        })
        assert response.status_code == 201

def test_partial_update_validation():
    with app.test_client() as client:
        client.post('/users', json={
            'name': 'Update',
            'lastname': 'Tester'
        })

        response = client.patch('/users/1', json={
            'name': 'NewName',
            'lastname': 'NewLastname'
        })
        assert response.status_code == 400

        response = client.patch('/users/1', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400

        name_response = client.patch('/users/1', json={
            'name': 'NewName'
        })
        assert name_response.status_code == 204

        lastname_response = client.patch('/users/1', json={
            'lastname': 'NewLastname'
        })
        assert lastname_response.status_code == 204