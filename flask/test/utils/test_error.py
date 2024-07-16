import pytest
from api.v1.utils.error import InvalidAPIUsage


class TestInvalidAPIUsage:
    def test_init_default_status_code(self):
        exception = InvalidAPIUsage("Test message")
        assert exception.message == "Test message"
        assert exception.status_code == 400
        assert exception.payload is None

    def test_init_custom_status_code(self):
        exception = InvalidAPIUsage("Test message", status_code=404)
        assert exception.message == "Test message"
        assert exception.status_code == 404
        assert exception.payload is None

    def test_init_with_payload(self):
        payload = {"key": "value"}
        exception = InvalidAPIUsage("Test message", payload=payload)
        assert exception.message == "Test message"
        assert exception.status_code == 400
        assert exception.payload == payload

    def test_to_dict(self):
        exception = InvalidAPIUsage("Test message", status_code=404)
        expected_dict = {
            "error": {
                "message": "Test message",
                "code": 404
            }
        }
        assert exception.to_dict() == expected_dict
