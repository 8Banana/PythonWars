#!/usr/bin/env python3


class CodeChallenge(object):
    ATTR_KEYS = [
        "success",
        "name",
        "slug",
        "description",
        "author",
        "rank"
        # skipping "averageCompletion",
        "tags",
    ]

    def __init__(self, json_data):
        for key in ATTR_KEYS:
            setattr(self, key, json_data[key])
        self.average_completion = json_data["averageCompletion"]
        self.project_id = json_data["session"]["projectId"]
        self.solution_id = json_data["session"]["solutionId"]
        self.setup = json_data["session"]["setup"]
        self.example_fixture = json_data["session"]["exampleFixture"]
        self.code = json_data["session"]["code"]
