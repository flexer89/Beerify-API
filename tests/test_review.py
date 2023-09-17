from fastapi.testclient import TestClient
from unittest import mock
from http import HTTPStatus
from main import app
from tests.conftest import (
    fixture_beer_name,
    fixture_alcohol_amount,
    fixture_review_id,
    fixture_rating_value,
    fixture_description,
    fixture_added_date,
    fixture_limit
)

client = TestClient(app)


def test_add_review(beer_name, description, alcohol_amout, rating_value, review_id, added_date):
    response_data = {"id": review_id,
                     "name": beer_name,
                     "description": description,
                     "alcohol": alcohol_amout,
                     "rating": rating_value,
                     "added": added_date}

    with mock.patch("databases.Database.execute", return_value=review_id):
        params = {
            "name": beer_name,
            "description": description,
            "alcohol": alcohol_amout,
            "rating": rating_value
        }
        response = client.post("/review/add", params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == response_data


def test_get_reviews_by_rating(review_id, beer_name, rating_value, alcohol_amout,
                               description, added_date, limit):

    expected_data = [{
            "id": review_id,
            "name": beer_name,
            "rating": rating_value,
            "alcohol": alcohol_amout,
            "description": description,
            "added": added_date,
        }
    ]

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):
        params = {
            "limit": limit,
            "sort_by": "rating"
        }
        response = client.get("/review/get/all", params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_get_reviews_by_alcohol(review_id, beer_name, rating_value, alcohol_amout,
                                description, added_date, limit):

    expected_data = [{
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }]

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):
        params = {
            "limit": limit,
            "sort_by": "alcohol"
        }
        response = client.get("/review/get/all", params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_get_reviews_by_name(review_id, beer_name, rating_value, alcohol_amout,
                             description, added_date, limit):

    expected_data = [{
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }]

    with mock.patch("databases.Database.fetch_all", return_value=expected_data):
        params = {
            "limit": limit,
            "sort_by": "name"
        }
        response = client.get("/review/get/all", params=params)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_get_review_by_id(review_id, beer_name, rating_value, alcohol_amout,
                          description, added_date):

    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_one", return_value=expected_data):
        response = client.get(f"/review/get-by-id/{review_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_get_review_by_name(review_id, beer_name, rating_value, alcohol_amout,
                            description, added_date):

    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.fetch_one", return_value=expected_data):
        response = client.get(f"/review/get-by-name/{beer_name}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_update_review(review_id, beer_name, rating_value, alcohol_amout,
                       description, added_date):

    expected_data = {
        "id": review_id,
        "name": beer_name,
        "rating": rating_value,
        "alcohol": alcohol_amout,
        "description": description,
        "added": added_date
    }

    with mock.patch("databases.Database.execute"):
        response = client.put(
            f"/review/edit/{review_id}", params=expected_data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data


def test_delete_review(review_id):

    expected_data = {
        "message": "Review deleted successfully"
    }

    with mock.patch("databases.Database.execute", return_value=1):
        response = client.delete(f"/review/delete/{review_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_data
