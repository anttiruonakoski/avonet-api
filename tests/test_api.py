from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_bird():
    response = client.get("/bird/1")
    assert response.status_code == 200
    
def test_get_bird_invalid_id():
    response = client.get("/bird/999999")
    assert response.status_code == 404


def test_get_birds():
    response = client.get("/birds/")
    assert response.status_code == 200


def test_get_birds_all():
    response = client.get("/birds/all?limit=100")
    assert response.status_code == 200
