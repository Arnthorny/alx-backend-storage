#!/usr/bin/env python3
"""
Write a Python function that inserts a new document in a collection based on
kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Python function

    Args:
        mongo_collection(`object`): A mongo collection object.

    Returns:
        The ObjectId of newly created document
    """
    new_ins = mongo_collection.insert_one(kwargs)
    return new_ins.inserted_id
