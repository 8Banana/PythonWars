#!/usr/bin/env python3
import inflection
import requests


_GET_USER_URL = "https://codewars.com/api/v1/users/{}"
_GET_CODE_CHALLENGE_URL = "https://www.codewars.com/api/v1/code-challenges/{}"
_TRAIN_NEXT_CODE_CHALLENGE_URL = "https://www.codewars.com/api/v1/code-challenges/{}/train"
_TRAIN_CODE_CHALLENGE_URL = "https://www.codewars.com/api/v1/code-challenges/{}/{}/train"
_ATTEMPT_SOLUTION_URL = "https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt"
_FINALIZE_SOLUTION_URL = "https://www.codewars.com/api/v1/code-challenges/projects/{}/solutions/{}/finalize"


class CodeWars:
    """The main API class.

    It's recommended to read the CodeWars documentation at
    https://dev.codewars.com/. Most methods return Python dictionaries.
    """

    def __init__(self, api_key=None):
        """Initialize the API."""
        self.api_key = api_key
        self.session = requests.Session()
        if api_key is not None:
            self.session.headers["Authorization"] = api_key

    def _request_json(self, method, url, **kwargs):
        """Perform a request, and return its JSON content as a dictionary.

        Since the author of this method fears mixedCase, he would die if
        the responses would be like in the CodeWars API documentation.
        That's why a huge third party dependency is used just for
        converting the keys of the resulting dictionary from mixedCase
        to under_scores.
        """
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return {inflection.underscore(k): v
                for k, v in response.json().items()}

    def get_user(self, id_or_username):
        """Return information about a specific user.

        See also: https://dev.codewars.com/#get-user
        """
        return self._request_json("get", _GET_USER_URL.format(id_or_username))

    def get_code_challenge(self, id_or_slug):
        """Return information about a specific code challenge (kata).

        See also: https://dev.codewars.com/#get-code-challenge
        """
        return self._request_json("get",
                                  _GET_CODE_CHALLENGE_URL.format(id_or_slug))

    def train_next_code_challenge(self, language, strategy="default", peek=False):
        """Begin a new training session for next kata in the training queue.

        See also: https://dev.codewars.com/#post-train-next-code-challenge
        """
        return self._request_json("post",
                                  _TRAIN_NEXT_CODE_CHALLENGE_URL.format(language),
                                  data={"strategy": strategy, "peek": peek})

    def train_code_challenge(self, id_or_slug, language):
        """Begin a new training session for the next kata.

        See also: https://dev.codewars.com/#post-train-code-challenge
        """
        return self._request_json("post",
                                  _TRAIN_CODE_CHALLENGE_URL.format(id_or_slug, language))

    def attempt_solution(self, project_id, solution_id, code, output_format="html"):
        """Submit a solution to be validated by the test cases.

        See also: https://dev.codewars.com/#post-attempt-solution
        """
        return self._request_json("post",
                                  _ATTEMPT_SOLUTION_URL.format(project_id, solution_id),
                                  data={"code": code,
                                        "output_format": output_format})

    def finalize_solution(self, project_id, solution_id):
        """Finalize the previously submitted solution.

        See also: https://dev.codewars.com/#post-attempt-solution
        """
        return self._request_json("post",
                                  _FINALIZE_SOLUTION_URL.format(project_id, solution_id))
