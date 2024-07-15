#!/usr/bin/env python3
"""
Inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    A function that inserts a new document in a collection based on kwargs.

    :param mongo_collection: The collection in which to insert the document.
    :param **kwargs: Keyword arguments representing the document to be inserted.
    :return: The ID of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
