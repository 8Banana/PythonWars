#!/usr/bin/env python3
import unittest
import unittest.mock

# Because we also need the `pythonwars.pythonwars` constants.
from pythonwars import pythonwars


class TestCodeWars(unittest.TestCase):
    def setUp(self):
        self.codewars = pythonwars.CodeWars()

    @unittest.mock.patch("pythonwars.CodeWars._request_json")
    def test_http_method(self, request_json):
        # This test validates that the arguments and calls for the
        # _request_json method don't change, because 90% of the time if you
        # change those you are bound to break something.
        self.codewars.get_user("8Banana")
        request_json.assert_called_with("get",
                                        pythonwars._GET_USER_URL.format("8Banana"))


if __name__ == "__main__":
    unittest.main()
