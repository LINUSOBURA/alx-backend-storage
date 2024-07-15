#!/usr/bin/env python3
"""
Lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    """
    collection = mongo_collection
    mlist = collection.find()
    if mlist:
        return mlist
    else:
        return []
