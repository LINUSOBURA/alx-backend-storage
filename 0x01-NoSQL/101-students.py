#!/usr/bin/env python3
"""
101-students
"""


def top_students(mongo_collection):
    """
    Calculates the average score of each student in the collection and
    returns them in descending order of average score.

    Parameters:
        mongo_collection: A MongoDB collection containing student documents.

    Returns:
        A list of students sorted by their average scores.
    """
    pipeline = [{
        '$project': {
            'name': 1,
            'averageScore': {
                '$avg': '$topics.score'
            }
        }
    }, {
        '$sort': {
            'averageScore': -1
        }
    }]

    students = mongo_collection.aggregate(pipeline)
    return students
