#!/usr/bin/env python3


class Rank(object):
    ATTR_KEYS = [
        "rank",
        "name",
        "color",
        "score"
    ]

    def __init__(self, json_data):
        for key in self.ATTR_KEYS:
            setattr(self, key, json_data[key])


class User(object):
    ATTR_KEYS = [
        "username",
        "name",
        "honor",
        "clan",
        "leaderboardPosition",
        "skills",
    ]

    def __init__(self, json_data):
        for key in self.ATTR_KEYS:
            setattr(self, key, json_data[key])
        self.overall_rank = Rank(json_data["ranks"]["overall"])
        self.language_ranks = {}
        for language, rank_data in json_data["ranks"]["languages"].items():
            self.language_ranks[language] = Rank(rank_data)
        self.code_challenges = {
            "authored": json_data["codeChallenges"]["totalAuthored"],
            "completed": json_data["codeChallenges"]["totalCompleted"]
        }
