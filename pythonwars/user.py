#!/usr/bin/env python3
from .util import AttributesFromJSON


class Rank(AttributesFromJSON):
    attr_keys = [
        "rank",
        "name",
        "color",
        "score"
    ]


class User(AttributesFromJSON):
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
        self.overall_rank = Rank(json_data["ranks"]["overall"])
        self.language_ranks = {}
        for language, rank_data in json_data["ranks"]["languages"].items():
            self.language_ranks[language] = Rank(rank_data)
