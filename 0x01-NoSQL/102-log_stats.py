#!/usr/bin/env python3
"""
provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def log_statics():
    """
    A function that logs statistics related to Nginx logs stored in MongoDB. It counts the total number of logs, the number of logs for each HTTP method (GET, POST, PUT, PATCH, DELETE), and checks the status for GET requests with the path "/status".
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

    print(
        f"{number_of_logs} logs\nMethods:\n\tmethod GET: {methods_GET}\n\tmethod POST: {methods_POST}\
			\n\tmethod PUT: {methods_PUT}\n\tmethod PATCH: {methods_PATCH}\
				\n\tmethod DELETE: {methods_DELETE}\n{status_check} status check")
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_statics()
