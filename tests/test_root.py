from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app

client = TestClient(app)

def test_root():
    response_data = {
        "health": "OK",
        "openapiapi documentation url":"/docs",
        "redoc documentation url ": "/redoc"
    }
    
    response = client.get("/")
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == response_data
