#!/usr/bin/env python3
"""
This module contains the Cache class
"""
import uuid
import redis
from typing import Any, Union, Callable
from functools import wraps


def count_calls(f):
    """
    Decorator function
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        self._redis.incr(f.__qualname__)
        return f(self, *args, **kwargs)
    return wrapper


def call_history(f):
    """
    Decorator function
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function
        """
        ip_key = "{}:inputs".format(f.__qualname__)
        op_key = "{}:outputs".format(f.__qualname__)

        self._redis.rpush(ip_key, str(args))
        ret_val = f(self, *args, **kwargs)
        self._redis.rpush(op_key, ret_val)

        return ret_val
    return wrapper


def replay(fn: Callable[[str], Any]) -> None:
    """
    Function to display the history of calls of a particular fn.

    Args:
        fn(`obj`): Function to be replayed
    """
    r = redis.Redis()
    inputs = r.lrange("{}:inputs".format(fn.__qualname__), 0, -1)
    outputs = r.lrange("{}:outputs".format(fn.__qualname__), 0, -1)

    print("Cache.store was called {} times:".format(len(inputs)))
    for ip, op in zip(inputs, outputs):
        print("Cache.store(*{}) -> {}".format(ip.decode("utf-8"),
                                              op.decode("utf-8")))


class Cache:
    """
    This class allows us access a redis instance.
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[int, float, str, bytes]) -> str:
        """
        Generate a random key (e.g. using uuid) and use it to store data in
        Redis.

        Args:
            data: Input data to be stored in Redis

        Return:
            (`str`): String containing randomly generated key
        """
        new_k = str(uuid.uuid4())
        if self._redis.set(new_k, data):
            return new_k

    def get(self, key: str, fn: Callable[[str], Any] = None) -> Any:
        """
        Get redis stored value in appropriate python format
        """
        val = self._redis.get(key)
        if not val:
            return None
        elif fn == int:
            return int(val)
        elif fn == str:
            return str(val)
        elif type(fn).__name__ == 'function':
            return fn(val)
        else:
            return val

    def get_str(self, key, fn=str):
        """
        Automatically parametrize Cache.get with string callable
        """
        return self.get(key, fn)

    def get_int(self, key, fn=int):
        """
        Automatically parametrize Cache.get int callable.
        """
        return self.get(key, fn)
