"""
A module for dealing with the CodeWars API via the CodeWars class.
"""
from __future__ import print_function

import time

import inflection
import requests


_API_URL = "http://codewars.com/api/v1/"
_GET_USER_URL = _API_URL + "users/{}"
_GET_CODE_CHALLENGE_URL = _API_URL + "code-challenges/{}"
_TRAIN_NEXT_CODE_CHALLENGE_URL = _API_URL + "code-challenges/{}/train"
_TRAIN_CODE_CHALLENGE_URL = _API_URL + "code-challenges/{}/{}/train"
_ATTEMPT_SOLUTION_URL = (_API_URL + "code-challenges/projects/:project_id/"
                         "solutions/:solution_id/attempt")
_FINALIZE_SOLUTION_URL = (_API_URL + "code-challenges/projects/{}/"
                          "solutions/{}/finalize")
_GET_DEFERRED_RESPONSE_URL = _API_URL + "deferred/{}"


class APIError(Exception):
    """This is raised when an error related to the API is detected."""


class CodeWars:
    """
    The class that handles the CodeWars API.

    Some methods can be used without passing an api_key to __init__, such as
    `get_user`.
    Whenever a method would return a camelCase key, this class turns it into
    a snake_case key.
    """

    def __init__(self, api_key=None, user_agent=None, use_camel_case=False):
        """
        Initalize a CodeWars instance.

        Arguments:
            api_key(str or None): Your API key.
            use_camel_case(bool): If to use camelCase keys or snake_case.
        """
        self.session = requests.Session()
        self.use_camel_case = use_camel_case
        if user_agent is not None:
            self.session.headers["User-Agent"] = user_agent
        else:
            self.session.headers["User-Agent"] = "8banana tui"
        if api_key is not None:
            self.session.headers["Authorization"] = api_key
        self._previous_deferred_response = 0

    def _request_json(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        if self.use_camel_case:
            return response.json()
        else:
            return {inflection.underscore(k): v
                    for k, v in response.json().items()}

    def get_user(self, id_or_username):
        """
        Get information about an user.

        More information:
            http://dev.codewars.com/#get-user
        """
        return self._request_json("get", _GET_USER_URL.format(id_or_username))

    def get_code_challenge(self, id_or_slug):
        """
        Get information about a code challenge.

        More information:
            http://dev.codewars.com/#get-code-challenge
        """
        return self._request_json(
            "get",
            _GET_CODE_CHALLENGE_URL.format(id_or_slug),
        )

    def train_next_code_challenge(self, language,
                                  strategy="default", peek=False):
        """
        Start a new, random, code challenge.

        WARNING: If peek is False, this method starts a hidden timer to track
        average completion time.
        More information:
            http://dev.codewars.com/#post-train-next-code-challenge
        """
        return self._request_json(
            "post",
            _TRAIN_NEXT_CODE_CHALLENGE_URL.format(language),
            data={"strategy": strategy, "peek": peek},
        )

    def train_code_challenge(self, id_or_slug, language):
        """
        Start a specific code challenge.

        WARNING: If peek is False, this method starts a hidden timer to track
        average completion time.
        More information:
            http://dev.codewars.com/#post-train-code-challenge
        """
        return self._request_json(
            "post",
            _TRAIN_CODE_CHALLENGE_URL.format(id_or_slug, language),
        )

    def attempt_solution(self, project_id, solution_id, code,
                         output_format="html"):
        """
        Submit a potential solution to a code challenge.

        More information:
            http://dev.codewars.com/#post-attempt-solution
        """
        return self._request_json(
            "post",
            _ATTEMPT_SOLUTION_URL.format(project_id, solution_id),
            data={"code": code, "output_format": output_format},
        )

    def finalize_solution(self, project_id, solution_id):
        """
        Finalize a code challenge previously sent by CodeWars.attempt_solution.

        More information:
            http://dev.codewars.com/#post-finalize-solution
        """
        return self._request_json(
            "post",
            _FINALIZE_SOLUTION_URL.format(project_id, solution_id),
        )

    def deferred_response(self, dmid):
        """Poll for a deferred response."""
        if time.time() - self._previous_deferred_response < 0.5:
            raise APIError("polling should not be performed more than "
                           "twice a second")
        self._previous_deferred_response = time.time()
        return self._request_json(
            'get', _GET_DEFERRED_RESPONSE_URL.format(dmid),
        )
