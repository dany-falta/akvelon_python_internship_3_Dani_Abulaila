TRANSACTION_ENDPOINT = '/finance'

""" Transaction route tests"""
def test_transaction_post(client):
    new_transaction_json = {"user_id": 1, "tr_amount": 42.03}
    response = client.post(f"{TRANSACTION_ENDPOINT}/create_transaction", json=new_transaction_json)
    assert response.status_code == 200


def test_transaction_error(client):
    incorrect_fields_json = {"user_id": 1, "tr_amount": 0}
    response = client.post(f"{TRANSACTION_ENDPOINT}/create_transaction", json=incorrect_fields_json)
    assert response.status_code == 422


def test_transaction_post_short_error(client):
    missing_user_json = {"user_id": 412, "tr_amount": 10}
    response = client.post(f"{TRANSACTION_ENDPOINT}/create_user", json=missing_user_json)
    assert response.status_code == 404


def test_transaction_put(client):
    update_transaction_json = {"transaction_id": "2", "tr_amount": -22.09}
    response = client.put(f"{TRANSACTION_ENDPOINT}/update_transaction", json=update_transaction_json)
    assert response.status_code == 200


def test_transaction_put_error(client):
    future_transaction_json = {"transaction_id": "2", "tr_date": "2022-11-12"}
    response = client.put(f"{TRANSACTION_ENDPOINT}/update_transaction", json=future_transaction_json)
    assert response.status_code == 422


def test_get_all_transaction(client):
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_transactions")
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_one_transaction(client):
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_transactions_by_id", json={"transaction_id": 1})
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_one_transaction_error(client):
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_transactions_by_id", json={"transaction_id": 100})
    assert response.status_code == 404


def test_get_user_transactions(client):
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_user_transactions", json={"user_id": 2, "sort": "By date"})
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_user_transactions_error(client):
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_user_transactions", json={"user_id": 100})
    assert response.status_code == 404


def test_get_user_transactions_by_date(client):
    date_transaction_json = {"user_id": "2", "start_date": "2020-11-12", "end_date": "2021-12-20"}
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_user_transactions_by_date", json=date_transaction_json)
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_user_transactions_by_date_error(client):
    date_transaction_json = {"user_id": "20", "start_date": "2020-11-12", "end_date": "2020-12-20"}
    response = client.get(f"{TRANSACTION_ENDPOINT}/view_user_transactions_by_date", json=date_transaction_json)
    assert response.status_code == 404


def test_transaction_delete(client):
    response = client.delete(f"{TRANSACTION_ENDPOINT}/delete_transaction", json={"transaction_id": 4})
    assert response.status_code == 200


def test_transaction_delete_error(client):
    response = client.delete(f"{TRANSACTION_ENDPOINT}/delete_transaction", json={"transaction_id": 400})
    assert response.status_code == 404
