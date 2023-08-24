from fastapi.testclient import TestClient
from main import app
from app.models.review import Review
from app.db.database import database
from unittest import mock
from unittest.mock import MagicMock
import pytest

client = TestClient(app)


def test_search_by_alcohol_found():
    response_data = {"id": 1, "name": "Żywiec", "alcohol": 5}

    with mock.patch("databases.Database.fetch_all", return_value=response_data):

        response = client.get("/search/by-alcohol?alcohol=5")

        assert response.status_code == 200
        assert response.json() == response_data


def test_search_by_alcohol_not_found():
    with mock.patch("databases.Database.fetch_all", return_value=None):

        response = client.get("/search/by-alcohol?alcohol=1.0")

        assert response.status_code == 404
        assert response.json() == {
            "detail": "Review with 1.0% of alcohol not found"}


def test_search_by_rating_found():
    response_mock = [{"id": 1, "rating": 4.0}]

    with mock.patch("databases.Database.fetch_all", return_value=response_mock):
        response = client.get("/search/by-rating?rating=4.0")
        assert response.status_code == 200
        assert response.json() == response_mock


def test_search_by_rating_not_found():
    with mock.patch("databases.Database.fetch_all", return_value=None):
        response = client.get("/search/by-rating?rating=4.0")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Review with 4.0 rating not found"}


def test_search_by_desc_found():
    response_mock = {
        "id": 1,
        "name": "Żywiec",
        "rating": 5,
        "alcohol": 0,
        "description": "test",
        "added": "2023-08-23T19:42:19"
    }

    with mock.patch("databases.Database.fetch_all", return_value=response_mock):
        response = client.get("/search/by-desc?desc=test")
        assert response.status_code == 200
        assert response.json() == response_mock


def test_search_by_desc_not_found():
    with mock.patch("databases.Database.fetch_all", return_value=None):
        response = client.get("/search/by-desc?desc=tasty")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Review with tasty in description not found"}
