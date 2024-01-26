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
        """
        Wrapper Function
        """
        c_key = "count:{{{}}}".format(url)
        r.incr(c_key)
        return f(url, *args, **kwargs)
    return wrapper


@url_tracker  # type: ignore
def get_page(url: str) -> str:
    """
    Get Page Function
    """
    cache_url = r.get(url)
    if not cache_url:
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            with r.pipeline() as pipe:
                pipe.set(url, req.text)
                pipe.expire(url, 10)
                pipe.execute()
            return req.text
    return cache_url
