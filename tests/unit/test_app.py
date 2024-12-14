from app.app import find_user_by_id, users_db

def test_find_user_by_id():
    users_db.clear()

    test_user = {
        'id': 1,
        'name': 'Test',
        'lastname': 'User'
    }
    users_db.append(test_user)

    found_user = find_user_by_id(1)
    assert found_user is not None
    assert found_user == test_user

    not_found_user = find_user_by_id(999)
    assert not_found_user is None

def test_user_id_generation():
    users_db.clear()

    first_user = {
        'id': len(users_db) + 1,
        'name': 'First',
        'lastname': 'User'
    }
    users_db.append(first_user)
    assert first_user['id'] == 1

    second_user = {
        'id': len(users_db) + 1,
        'name': 'Second',
        'lastname': 'User'
    }
    users_db.append(second_user)
    assert second_user['id'] == 2

    assert len(users_db) == 2
    assert users_db[0]['name'] == 'First'
    assert users_db[1]['name'] == 'Second'