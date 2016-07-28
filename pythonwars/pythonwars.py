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

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key is not None:
            self.session.headers.update({
                "Authorization": api_key,
            })

    def _request_json(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return {inflection.underscore(k): v
                for k, v in response.json().items()}

    def get_user(self, id_or_username):
        return self._request_json("get", _GET_USER_URL.format(id_or_username))

    def get_code_challenge(self, id_or_slug):
        return self._request_json(
            "get",
            _GET_CODE_CHALLENGE_URL.format(id_or_slug),
        )

    def train_next_code_challenge(self, language, strategy="default", peek=False):
        return self._request_json(
            "post",
            _TRAIN_NEXT_CODE_CHALLENGE_URL.format(language),
            data={"strategy": strategy, "peek": peek},
        )

    def train_code_challenge(self, id_or_slug, language):
        return self._request_json(
            "post",
            _TRAIN_CODE_CHALLENGE_URL.format(id_or_slug, language),
        )

    def attempt_solution(self, project_id, solution_id, code,
                         output_format="html"):
        return self._request_json(
            "post",
            _ATTEMPT_SOLUTION_URL.format(project_id, solution_id),
            data={"code": code, "output_format": output_format},
        )

    def finalize_solution(self, project_id, solution_id):
        return self._request_json(
            "post",
            _FINALIZE_SOLUTION_URL.format(project_id, solution_id),
        )
