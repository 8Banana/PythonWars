#!/usr/bin/env python3
import requests

from .user import User
from .codechallenge import TrainingCodeChallenge, CodeChallengeInfo


_GET_USER_URL = "https://codewars.com/api/v1/users/{}"
_GET_CODE_CHALLENGE_URL = "https://www.codewars.com/api/v1/code-challenges/{}"
_TRAIN_NEXT_CODE_CHALLENGE_URL = "https://www.codewars.com/api/v1/code-challenges/{}/train"
_TRAIN_CODE_CHALLENGE_URL = "https://www.codewars.com/api/v1/code-challenges/{}/{}/train"
_ATTEMPT_SOLUTION_URL = "https://www.codewars.com/api/v1/code-challenges/projects/:project_id/solutions/:solution_id/attempt"
_FINALIZE_SOLUTION_URL = "https://www.codewars.com/api/v1/code-challenges/projects/{}/solutions/{}/finalize"


class CodeWars:

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key is not None:
            self.session.headers.update({
                "Authorization": api_key,
            })

    def _request_json(self, url, cls=None, **kwargs):
        # If you pass data, `.get` automatically becomes `.post`
        response = self.session.get(url, **kwargs)
        response.raise_for_status()
        if cls is None:
            return response.json()
        else:
            return cls(response.json())

    def get_user(self, id_or_username):
        return self._request_json(_GET_USER_URL.format(id_or_username), User)

    def get_code_challenge(self, id_or_slug):
        return self._request_json(_GET_CODE_CHALLENGE_URL.format(id_or_slug),
                                  CodeChallengeInfo)

    def train_next_code_challenge(self, language, strategy="default", peek=False):
        return self._request_json(_TRAIN_NEXT_CODE_CHALLENGE_URL.format(language),
                                  TrainingCodeChallenge,
                                  data={"strategy": strategy, "peek": peek})

    def train_code_challenge(self, id_or_slug, language):
        return self._request_json(_TRAIN_CODE_CHALLENGE_URL.format(id_or_slug, language),
                                  TrainingCodeChallenge)

    def attempt_solution(self, project_id, solution_id, code, output_format="html"):
        return self._request_json(_ATTEMPT_SOLUTION_URL.format(project_id, solution_id),
                                  None,
                                  data={"code": code,
                                        "output_format": output_format})

    def finalize_solution(self, project_id, solution_id):
        return self._request_json(_FINALIZE_SOLUTION_URL.format(project_id, solution_id))
