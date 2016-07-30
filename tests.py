#!/usr/bin/env python3
import unittest
try:
    from unittest import mock
except ImportError:
    # For all versions of python less than 3.3
    import mock

# Because we also need the `pythonwars.pythonwars` constants.
from pythonwars import pythonwars


class TestCodeWars(unittest.TestCase):
    def setUp(self):
        self.codewars = pythonwars.CodeWars()

    @mock.patch("pythonwars.CodeWars._request_json")
    def test_http_method(self, request_json):
        # This test validates that the arguments and calls for the
        # _request_json method don't change, because 90% of the time if you
        # change those you are bound to break something.
        self.codewars.get_user("8Banana")
        request_json.assert_called_with("get",
                                        pythonwars._GET_USER_URL.format("8Banana"))

    def test_https(self):
        self.assertFalse(pythonwars._API_URL.startswith("https"))


if __name__ == "__main__":
    unittest.main()
