import pytest

import _setpath
from app.app import *


def test_get_request_valid():
    params = {"xy": "-97.7509434127,30.27618598841"}
    request, response = app.test_client.get("/v1/trips", params=params)
    assert response.status == 200


def test_invalid_datetime():
    params = {
        "xy": "-97.7509434127,30.27618598841",
        "start_time": "pizza",
        "end_time": 1542034074000
    }

    request, response = app.test_client.get("/v1/trips", params=params)
    assert response.status == 500


def test_get_datetime():
    params = {
        "xy": "-97.7509434127,30.27618598841",
        "start_time": 1541947674000,
        "end_time": 1542034074000
    }

    request, response = app.test_client.get("/v1/trips", params=params)

    assert response.status == 200
    assert len(response.json["features"]["features"]) > 0


def test_get_query_geom_point():
    assert isinstance(get_query_geom([(125.6, 10.1)]), Point)


def test_get_query_geom_polygon():
    assert isinstance(
        get_query_geom([(125.6, 10.1), (125.6, 10.1), (125.6, 10.1), (125.6, 10.1)]),
        polygon.PolygonAdapter,
    )


def test_parse_flow():
    assert parse_flow({"flow": "origin"}) == "origin"
    assert parse_flow({"flow": None}) == "origin"
    assert parse_flow({"flow": "destination"}) == "destination"

    with pytest.raises(exceptions.ServerError):
        parse_flow({"flow": "pizza"})


def test_parse_mode():
    assert parse_mode({"mode": "scooter"}) == "scooter"
    assert parse_mode({"mode": "all"}) == "all"
    assert parse_mode({"mode": None}) == "all"
    assert parse_mode({"mode": "bicycle"}) == "bicycle"

    with pytest.raises(exceptions.ServerError):
        parse_mode({"mode": "pizza"})
