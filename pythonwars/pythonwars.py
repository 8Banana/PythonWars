"""
This module just contains the CodeWars class, which is better explained in its
docstring.
"""
import inflection
import requests


_API_URL = "https://codewars.com/api/v1/"
_GET_USER_URL = _API_URL + "users/{}"
_GET_CODE_CHALLENGE_URL = _API_URL + "code-challenges/{}"
_TRAIN_NEXT_CODE_CHALLENGE_URL = _API_URL + "code-challenges/{}/train"
_TRAIN_CODE_CHALLENGE_URL = _API_URL + "code-challenges/{}/{}/train"
_ATTEMPT_SOLUTION_URL = (_API_URL + "code-challenges/projects/:project_id/"
                         "solutions/:solution_id/attempt")
_FINALIZE_SOLUTION_URL = (_API_URL + "code-challenges/projects/{}/"
                          "solutions/{}/finalize")


class CodeWars:
    """
    The class that handles the CodeWars API.
    Some methods can be used without passing an api_key to __init__, such as
    `get_user`.
    Whenever a method would return a camelCase key, this class turns it into
    a snake_case key.
    """
    def __init__(self, api_key=None, 
                user_agent='8Banana TUI' 
                *, 
                use_camel_case=False):

        self.use_camel_case = use_camel_case
        self.session = requests.Session()
        self.session.headers['User-agent'] = user_agent
        if api_key is not None:
            self.session.headers["Authorization"] = api_key

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
        Gets information about an user.
        More information:
            http://dev.codewars.com/#get-user
        """
        return self._request_json("get", _GET_USER_URL.format(id_or_username))

    def get_code_challenge(self, id_or_slug):
        """
        Gets infromation about a code challenge.
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
        Starts a new, random, code challenge.
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
        Starts a specific code challenge.
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
        Submits a potential solution to a code challenge.
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
        Finalizes a code challenge sent before by CodeWars.attempt_solution
        More information:
            http://dev.codewars.com/#post-finalize-solution
        """
        return self._request_json(
            "post",
            _FINALIZE_SOLUTION_URL.format(project_id, solution_id),
        )
