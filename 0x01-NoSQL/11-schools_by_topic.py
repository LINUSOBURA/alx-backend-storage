#!/usr/bin/env python3
"""
 returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
    mongo_collection: pymongo collection object
    topic (string): topic searched

    Returns:
    List of schools matching the topic
    """

    topic_filter_bySchool = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter_bySchool)]

    #return mongo_collection.find({"topic": topic})
