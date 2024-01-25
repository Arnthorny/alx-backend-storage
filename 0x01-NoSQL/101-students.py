#!/usr/bin/env python3
"""
Write a Python function that returns all students sorted by average score

The top must be ordered
The average score must be part of each item returns with key = averageScore
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Python function

    Args:
        mongo_collection(`object`): A mongo collection object.
    """
    all_fields = list(mongo_collection.aggregate([
        {"$addFields": {"averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ]))
    return all_fields
