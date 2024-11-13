import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_not_found(client):
    response = client.get('/')
    assert response.status_code == 404
    assert b'error: route not found' in response.data
