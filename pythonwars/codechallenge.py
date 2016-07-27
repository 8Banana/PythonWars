#!/usr/bin/env python3
from .util import AttributesFromJson


class TrainingCodeChallenge(AttributesFromJson):
    attr_keys = [
        "success",
        "name",
        "slug",
        "description",
        "author",
        "rank",
        "averageCompletion",
        "tags",
        "session/projectId",
        "session/solutionId",
        "session/setup",
        "session/exampleFixture",
        "session/code",
    ]

class CodeChallengeInfo(AttributesFromJson):
    attr_keys = [
        "id",
        "name",
        "slug",
        "category",
        "publishedAt",
        "approvedAt",
        "languages",
        "url",
        "rank",
        "createdBy",
        "approvedBy",
        "description",
        "totalAttempts",
        "totalCompleted",
        "totalStars",
        "tags",
    ]
