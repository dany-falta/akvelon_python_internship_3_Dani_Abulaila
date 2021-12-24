USER_ENDPOINT = '/user'

""" User route tests"""
def test_users_post(client):
    new_user_json = {"first_name": "Jamey","last_name": "Ааass",  "email": "arax@tesat.com", "password": "test1234"}
    response = client.post(f"{USER_ENDPOINT}/create_user", json=new_user_json)
    assert response.status_code == 200


def test_users_post_error(client):
    missing_fields_json = {"first_name": "Drake", "email": "fail@test.com", "password": "fail1234"}
    response = client.post(f"{USER_ENDPOINT}/create_user", json=missing_fields_json)
    assert response.status_code == 400


def test_users_post_short_error(client):
    short_fields_json = {"first_name": "Dr", "last_name": "Аdsf", "email": "tyy@test.com", "password": "fail1234"}
    response = client.post(f"{USER_ENDPOINT}/create_user", json=short_fields_json)
    assert response.status_code == 422


def test_users_put(client):
    update_user_json = {"user_id": "2", "last_name": "updated"}
    response = client.put(f"{USER_ENDPOINT}/update_user", json=update_user_json)
    assert response.status_code == 200


def test_users_put_error(client):
    short_user_field_json = {"user_id": "2", "last_name": "a"}
    response = client.put(f"{USER_ENDPOINT}/update_user", json=short_user_field_json)
    assert response.status_code == 422


def test_get_all_users(client):
    response = client.get(f"{USER_ENDPOINT}/view_users")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_one_user(client):
    response = client.get(f"{USER_ENDPOINT}/view_user_by_id", json={"user_id": 1})
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_one_user_error(client):
    response = client.get(f"{USER_ENDPOINT}/view_user_by_id", json={"user_id": 100})
    assert response.status_code == 404


def test_users_delete(client):
    response = client.delete(f"{USER_ENDPOINT}/delete_user", json={"user_id": 4})
    assert response.status_code == 200


def test_users_delete_error(client):
    response = client.delete(f"{USER_ENDPOINT}/delete_user", json={"user_id": 400})
    assert response.status_code == 404
