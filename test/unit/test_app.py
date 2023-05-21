import unittest.mock
from redis import ConnectionError


@unittest.mock.patch("page_tracker.app.redis")
def test_should_call_redis_incr(mock_redis, http_client):
    # GIVEN
    mock_redis.return_value.incr.return_value = 5

    # WHEN
    response = http_client.get("/")

    # THEN
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    mock_redis.return_value.incr.assert_called_once_with("page_views")


@unittest.mock.patch("page_tracker.app.redis")
def test_should_handle_redis_connection_error(mock_redis, http_client):
    # GIVEN
    mock_redis.return_value.incr.side_effect = ConnectionError

    # WHEN
    response = http_client.get("/")

    # THEN
    assert response.status_code == 500
    assert response.text == "Sorry, something went wrong!"
