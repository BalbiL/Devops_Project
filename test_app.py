import pytest
from app import app, redis_client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello(client):
    response = client.get("/")
    assert response.data == b"Hello, Redis World!"

def test_set_and_get(client):
    redis_client.flushdb()  # Nettoyer Redis avant le test
    response = client.post("/set", json={"key": "testkey", "value": "testvalue"})
    assert response.status_code == 200

    response = client.get("/get/testkey")
    assert response.json == {"key": "testkey", "value": "testvalue"}

