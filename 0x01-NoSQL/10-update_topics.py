#!/usr/bin/env python3
"""
 changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of all documents in the given mongo_collection that have the specified name.

    Parameters:
        mongo_collection (pymongo.collection.Collection): The collection to update.
        name (str): The name of the documents to update.
        topics (List[str]): The new topics to set for the documents.

    Returns:
        None
    """
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
