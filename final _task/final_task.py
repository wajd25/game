from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
from main import app  # Adjust import according to your project structure
from sqlalchemy.orm import Session
from models import Car  # Ensure this import matches your project structure

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    with patch('main.get_db') as mock:  # Adjust the path if necessary
        mock_session = MagicMock()
        mock.return_value = mock_session
        yield mock_session

def test_create_car(mock_db_session):
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    response = client.post("/cars/", json={"make": "Toyota", "model": "Corolla", "year": 2024})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2024}
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_retrieve_all_cars(mock_db_session):
    mock_db_session.query.return_value.all.return_value = [
        Car(id=1, make="Toyota", model="Corolla", year=2024),
        Car(id=2, make="Honda", model="Civic", year=2023)
    ]
    
    response = client.get("/cars/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['make'] == "Toyota"

def test_retrieve_specific_car(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = Car(id=1, make="Toyota", model="Corolla", year=2024)
    
    response = client.get("/cars/1")
    assert response.status_code == 200
    assert response.json()['make'] == "Toyota"

def test_update_car(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = Car(id=1, make="Toyota", model="Corolla", year=2024)
    mock_db_session.commit = MagicMock()

    response = client.put("/cars/1", json={"make": "Toyota", "model": "Camry", "year": 2025})
    assert response.status_code == 200
    assert response.json()['model'] == "Camry"
    mock_db_session.commit.assert_called_once()

def test_delete_car(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = Car(id=1, make="Toyota", model="Corolla", year=2024)
    mock_db_session.delete = MagicMock()
    mock_db_session.commit = MagicMock()

    response = client.delete("/cars/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Car deleted"}
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
