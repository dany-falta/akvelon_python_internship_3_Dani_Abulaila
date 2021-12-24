""" Fibonacci route tests"""
def test_fibonacci_get(client):
    response = client.get("/fibonacci/9")
    assert response.status_code == 200
    assert response.json == 34
