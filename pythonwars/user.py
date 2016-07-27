#!/usr/bin/env python3
from .util import AttributesFromJson


__all__ = ["User", "UserLanguageRank", "CodeChallengeRank"]


class UserLanguageRank(AttributesFromJson):
    attr_keys = [
        "rank",
        "name",
        "color",
        "score"
    ]


class CodeChallengeRank(AttributesFromJson):
    attr_keys = [
        "id",
        "name",
        "color"
    ]


class User(AttributesFromJson):
    attr_keys = [
        "username",
        "name",
        "honor",
        "clan",
        "leaderboardPosition",
        "skills",
        "codeChallenges",
    ]

    def __init__(self, json_data):
        super().__init__(json_data)
        self.overall_rank = UserLanguageRank(json_data["ranks"]["overall"])
        self.language_ranks = {}
        for language, rank_data in json_data["ranks"]["languages"].items():
            self.language_ranks[language] = UserLanguageRank(rank_data)
