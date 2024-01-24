#!/usr/bin/env python3
"""
Write a Python function that returns the list of school having a specific
topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Python function

    Args:
        mongo_collection(`object`): A mongo collection object.
        topic(`str`): will be topic searched
    """
    return list(mongo_collection.find(
        {"topics": {"$all": [topic]}}
    ))
