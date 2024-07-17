#!/usr/bin/env python3
"""
Exercises
"""
from functools import wraps
from typing import Any, Callable, Optional
from uuid import uuid4

import redis

r = redis.Redis()


def count_calls(method: Callable) -> Callable:

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))
        return output

    return wrapper


class Cache:

    def __init__(self) -> None:
        """
        Initializes the Cache object by creating a Redis connection and flushing the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Any) -> str:
        """
        Store the data in the cache with a unique key.
        
        Parameters:
            data (Any): The data to be stored in the cache.

        Returns:
            str: The unique key under which the data is stored in the cache.
        """
        key = str(uuid4())
        r.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """
        Retrieves the value from the cache associated with the given key and applies a callback function to it.
        
        Parameters:
            key (str): The key to retrieve the value from the cache.
            fn (Callable): The callback function to be applied to the retrieved value.
        """
        result = self._redis.get(key)
        if result is not None and fn is not None:
            return fn(result)
        return result

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from the cache associated with the given key and converts it to a string.
        
        Parameters:
            key (str): The key to retrieve the string value from the cache.
        
        Returns:
            str: The string value associated with the key.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from the cache associated with the given key and converts it to an integer.
        
        Parameters:
            key (str): The key to retrieve the integer value from the cache.
        
        Returns:
            int: The integer value associated with the key.
        """
        return self.get(key, fn=int)