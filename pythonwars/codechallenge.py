#!/usr/bin/env python3
from .util import _AttributesFromJson


class CodeChallenge(_AttributesFromJson):
    ATTR_KEYS = [
        "success",
        "name",
        "slug",
        "description",
        "author",
        "rank"
        "averageCompletion",
        "tags",
        "session/projectId",
        "session/solutionId",
        "session/setup",
        "session/exampleFixture",
        "session/code",
    ]
