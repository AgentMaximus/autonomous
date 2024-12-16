import pytest
from fastapi.testclient import TestClient
from .fastapi_app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_natural_gas_prices():
    response = client.get("/natural_gas_prices")
    assert response.status_code == 200
    # Check if the response is a list of dictionaries
    assert isinstance(response.json(), list)
    if response.json():  # If there are any items, check the first one
        first_item = response.json()[0]
        assert isinstance(first_item, dict)