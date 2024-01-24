#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx logs stored in
MongoDB.

Database: logs
Collection: nginx
Display (same as the example):
"""
from pymongo import MongoClient


def main(nginx_logs):
    """
    Python function

    Args:
        nginx_logs(`object`): A mongo collection object.
    """
    total_logs = len(list(nginx_logs.find()))
    total_get_status = len(list(nginx_logs.find({"path": {"$eq": "/status"}})))

    print('{} logs'.format(total_logs))
    all_verbs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    all_meth_c = list(nginx_logs.aggregate([
        {"$match": {"method":
                    {"$in": ['GET', 'POST', 'PUT']}}
         },
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ]))

    print('Methods:')
    for verb in all_verbs:
        verb_count = [v['count'] for v in all_meth_c if v['_id'] == verb]
        verb_count = (verb_count and verb_count[0]) or 0
        print('\tmethod {}: {}'.format(verb, verb_count))
    print("{} status check".format(total_get_status))


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx
    main(nginx_logs)
