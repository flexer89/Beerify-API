from fastapi.testclient import TestClient
from http import HTTPStatus
from main import app
from unittest import mock
from tests.conftest import (
    fixture_beer_name,
    fixture_alcohol_amount,
    fixture_review_id,
    fixture_rating_value,
    fixture_description,
    fixture_added_date
)

client = TestClient(app)


def test_search_by_alcohol_found(review_id, beer_name, alcohol_amout):
    response_data = {"id": review_id,
                     "name": beer_name, "alcohol": alcohol_amout}

    with mock.patch("databases.Database.fetch_all", return_value=response_data):

        response = client.get(f"/search/by-alcohol?alcohol={alcohol_amout}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == response_data


def test_search_by_alcohol_not_found(alcohol_amout):
    with mock.patch("databases.Database.fetch_all", return_value=[]):

        response = client.get(f"/search/by-alcohol?alcohol={alcohol_amout}")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {
            "detail": f"Review with {alcohol_amout}% of alcohol not found"}


def test_search_by_rating_found(review_id, rating_value):
    response_mock = {"id": review_id, "rating": rating_value}

    with mock.patch("databases.Database.fetch_all", return_value=response_mock):
        response = client.get(f"/search/by-rating?rating={rating_value}")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == response_mock


def test_search_by_rating_not_found(rating_value):
    with mock.patch("databases.Database.fetch_all", return_value=[]):
        response = client.get(f"/search/by-rating?rating={rating_value}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {
            "detail": f"Review with {rating_value} rating not found"}


def test_search_by_desc_found(review_id, beer_name, rating_value,
                              alcohol_amout, description, added_date):
    response_mock = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_all", return_value=response_mock):
        response = client.get(f"/search/by-desc?desc={description}")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == response_mock


def test_search_by_desc_not_found(description):
    with mock.patch("databases.Database.fetch_all", return_value=[]):
        response = client.get(f"/search/by-desc?desc={description}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {
            "detail": f"Review with {description} in description not found"}
