#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx logs stored in
MongoDB.

Database: logs
Collection: nginx
Display (same as the example):
"""
from pymongo import MongoClient


def get_verb_count(nginx_logs, all_verbs):
    """
    This function returns a list containing an aggregate
    of all documents matching the given method + thier count
    """
    all_meth_c = list(nginx_logs.aggregate([
        {"$match": {"method":
                    {"$in": all_verbs}}
         },
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ]))
    return all_meth_c


def get_ip_count(nginx_logs):
    """
    This function a list of the top 10 of the most present IPs in the
    collection.
    """
    top_ips = list(nginx_logs.aggregate([
        {"$group": {"_id": "$ip",
                    "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]))
    return top_ips


def main(nginx_logs):
    """
    Python function

    Args:
        nginx_logs(`object`): A mongo collection object.
    """
    all_verbs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    total_logs = len(list(nginx_logs.find()))
    total_get_status = len(list(nginx_logs.find({"path": {"$eq": "/status"}})))

    print('{} logs'.format(total_logs))
    all_meth_c = get_verb_count(nginx_logs, all_verbs)
    print('Methods:')
    for verb in all_verbs:
        verb_count = [v['count'] for v in all_meth_c if v['_id'] == verb]
        verb_count = (verb_count and verb_count[0]) or 0
        print('\tmethod {}: {}'.format(verb, verb_count))
    print("{} status check".format(total_get_status))
    print("IPs:")
    top_ips = get_ip_count(nginx_logs)
    for ip in top_ips:
        print('\t{}: {}'.format(ip.get('_id'), ip.get('count')))


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx
    main(nginx_logs)
