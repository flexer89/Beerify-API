from pytest import fixture
from datetime import datetime


@fixture(name="beer_name")
def fixture_beer_name():
    return "test_beer_name"


@fixture(name="alcohol_amout")
def fixture_alcohol_amount():
    return 5.0


@fixture(name="review_id")
def fixture_review_id():
    return 1


@fixture(name="rating_value")
def fixture_rating_value():
    return 5.0


@fixture(name="description")
def fixture_description():
    return "test_description"


@fixture(name="added_date")
def fixture_added_date():
    date_format = "%Y-%m-%dT%H:%M:%S"
    formatted_date = datetime.now().strftime(date_format)
    return formatted_date


@fixture(name="limit")
def fixture_limit():
    return 1


@fixture(name="year")
def fixture_year():
    return 2023


@fixture(name="month")
def fixture_month():
    return 12
