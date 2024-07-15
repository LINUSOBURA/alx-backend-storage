#!/usr/bin/env python3
"""
provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def log_statics():
    """
    Logs statistics related to Nginx logs stored in MongoDB.

    This function connects to the MongoDB server at 'mongodb://127.0.0.1:27017'
    and retrieves the 'nginx' collection from the 'logs' database. It then counts
    the total number of logs, the number of logs for each HTTP method (GET, POST,
    PUT, PATCH, DELETE), and checks the status for GET requests with the path
    "/status".

    The function also retrieves the top 10 IP addresses that have made the most
    requests.

    Parameters:
        None

    Returns:
        None
    """

    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    number_of_logs = collection.count_documents({})
    methods_GET = collection.count_documents({"method": "GET"})
    methods_POST = collection.count_documents({"method": "POST"})
    methods_PUT = collection.count_documents({"method": "PUT"})
    methods_PATCH = collection.count_documents({"method": "PATCH"})
    methods_DELETE = collection.count_documents({"method": "DELETE"})

    status_check = collection.count_documents({
        "method": "GET",
        "path": "/status"
    })

    pipeline = [{
        "$group": {
            "_id": "$ip",
            "count": {
                "$sum": 1
            }
        }
    }, {
        "$sort": {
            "count": -1
        }
    }, {
        "$limit": 10
    }]

    top_ips = collection.aggregate(pipeline)

    print(f"{number_of_logs} logs")
    print("Methods:")
    print(f"\tmethod GET: {methods_GET}")
    print(f"\tmethod POST: {methods_POST}")
    print(f"\tmethod PUT: {methods_PUT}")
    print(f"\tmethod PATCH: {methods_PATCH}")
    print(f"\tmethod DELETE: {methods_DELETE}")
    print(f"{status_check} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_statics()
