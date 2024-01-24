#!/usr/bin/env python3
"""
Write a Python function that changes all topics of a school document based on
the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Python function

    Args:
        mongo_collection(`object`): A mongo collection object.
        name(`str`): will be the school name to update
        topics(`list`): (list of strings) will be the list of topics approached
        in the school
    """
    mongo_collection.update_one(
        {"name": name},
        {"$set": {"topics": topics}}
    )
