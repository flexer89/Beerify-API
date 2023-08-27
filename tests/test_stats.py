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
    fixture_added_date,
    fixture_month,
    fixture_year
)

client = TestClient(app)


def test_count_reviews():
    response_data = {"Reviews amount": 1}

    with mock.patch("databases.Database.fetch_val", return_value=1):

        response = client.get("/stats/count/")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == response_data


def test_average_rating():
    response_data = {"Average rating": 1}

    with mock.patch("databases.Database.fetch_val", return_value=1):

        response = client.get("/stats/average-rating/")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == response_data


def test_top_rated(review_id, beer_name, rating_value,
                   alcohol_amout, description, added_date):
    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):

        response = client.get(f"/stats/top-rated/1/")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_lowest_rated(review_id, beer_name, rating_value,
                      alcohol_amout, description, added_date):
    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):

        response = client.get(f"/stats/lowest-rated/1/")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_reviews_by_year(review_id, beer_name, rating_value,
                         alcohol_amout, description, added_date, year):
    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):

        response = client.get(f"/stats/reviews-by-year/{year}/")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_reviews_by_month(review_id, beer_name, rating_value,
                          alcohol_amout, description, added_date, year, month):
    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):

        response = client.get(f"/stats/reviews-by-month/{year}/{month}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data
