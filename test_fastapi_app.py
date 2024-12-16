import pytest
from fastapi.testclient import TestClient
from .fastapi_app import app
from unittest.mock import patch

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@patch('requests.get')
def test_get_natural_gas_prices(mock_get):
    # Configure the mock to return a response with an OK status
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"Some content"  # Mocked file content
    
    response = client.get("/natural_gas_prices")
    assert response.status_code == 200
    # Proceed with other assertions based on mocked return

    # Optionally look for a particular structure if you know it
    assert isinstance(response.json(), list)  # This would adjust based on what mocked data you returned