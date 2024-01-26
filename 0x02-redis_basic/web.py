#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function (prototype: def
get_page(url: str) -> str:). The core of the function is very simple. It uses
the requests module to obtain the HTML content of a particular URL and returns
it.

Start in a new file named web.py and do not reuse the code written in
exercise.py.

Inside get_page track how many times a particular URL was accessed in the key
"count:{url}" and cache the result with an expiration time of 10 seconds.
"""
import requests
from functools import wraps
import redis

r = redis.Redis()


def url_tracker(f):
    """
    Decorator function
    """
    @wraps(f)
    def wrapper(url, *args, **kwargs):
        key = "count:{{{}}}".format(url)
        with r.pipeline() as pipe:
            if not r.exists(key):
                print('here')
                pipe.set(key, 0)
                pipe.expire(key, 10)
            pipe.incr(key)
            pipe.execute()
        return f(url, *args, **kwargs)
    return wrapper


@url_tracker
def get_page(url: str) -> str:
    """
    Get Page Function
    """
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return r.text
