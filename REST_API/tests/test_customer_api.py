import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    return app.test_client()

@patch('services.customer_service.CustomerService.insert_customer')
def test_add_customer(mock_insert, client):
    mock_insert.return_value = {"message": "Customer added successfully"}
    response = client.post('/api/customers/', json={
        "CustomerID": "C001",
        "CustomerName": "John Doe",
        "Address": "123 Elm St",
        "City": "Somewhere",
        "PostalCode": "123456",
        "Country": "USA"
    })
    assert response.status_code == 201
