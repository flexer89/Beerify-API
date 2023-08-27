from pytest import fixture


@fixture(name="beer_name")
def fixture_beer_name():
    return "test_beer_name"


@fixture(name="alcohol_amout")
def fixture_alcohol_amount():
    return 9999.0


@fixture(name="review_id")
def fixture_review_id():
    return 1


@fixture(name="rating_value")
def fixture_rating_value():
    return 999.0


@fixture(name="description")
def fixture_description():
    return "test_description"


@fixture(name="added_date")
def fixture_added_date():
    return "test_added_date"


@fixture(name="limit")
def fixture_limit():
    return 9999


@fixture(name="year")
def fixture_year():
    return 1000


@fixture(name="month")
def fixture_month():
    return 1000
