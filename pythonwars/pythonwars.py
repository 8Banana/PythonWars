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

    def get_user(self, id_or_username):
        url = _GET_USER_URL.format(id_or_username)
        response = self.session.get(url)
        response.raise_for_status()
        return User(response.json())

    def get_code_challenge(self, id_or_slug):
        url = _GET_CODE_CHALLENGE_URL.format(id_or_slug)
        response = self.session.get(url)
        response.raise_for_status()
        return CodeChallengeInfo(response.json())

    def train_next_code_challenge(self, language, strategy="default", peek=False):
        url = _TRAIN_NEXT_CODE_CHALLENGE_URL.format(language)
        post_data = {
            "strategy": strategy,
            "peek": peek,
        }
        response = self.session.post(url, data=post_data)
        response.raise_for_status()
        return TrainingCodeChallenge(response.json())

    def train_code_challenge(self, id_or_slug, language):
        url = _TRAIN_CODE_CHALLENGE_URL.format(id_or_slug, language)
        response = self.session.post(url)
        response.raise_for_status()
        return TrainingCodeChallenge(response.json())

    def attempt_solution(self, project_id, solution_id, code, output_format="html"):
        url = _ATTEMPT_SOLUTION_URL.format(project_id, solution_id)
        post_data = {
            "code": code,
            "output_format": output_format,
        }
        response = self.session.post(url, data=post_data)
        response.raise_for_status()
        return response.json()

    def finalize_solution(self, project_id, solution_id):
        url = _FINALIZE_SOLUTION_URL.format(project_id, solution_id)
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()
