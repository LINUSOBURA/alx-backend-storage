#!/usr/bin/env python3
"""
Exercises
"""
from typing import Any, Callable
from uuid import uuid4

import redis

r = redis.Redis()


class Cache:

    def __init__(self) -> None:
        """
        Initializes the Cache object by creating a Redis connection and flushing the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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

    def get(self, key: str, fn: Callable):
        """
        Retrieves the value from the cache associated with the given key and applies a callback function to it.
        
        Parameters:
            key (str): The key to retrieve the value from the cache.
            fn (Callable): The callback function to be applied to the retrieved value.
        """
        fn(r.get(key))

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from the cache associated with the given key and converts it to a string.
        
        Parameters:
            key (str): The key to retrieve the string value from the cache.
        
        Returns:
            str: The string value associated with the key.
        """
        return str(self.get(key))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from the cache associated with the given key and converts it to an integer.
        
        Parameters:
            key (str): The key to retrieve the integer value from the cache.
        
        Returns:
            int: The integer value associated with the key.
        """
        return int(self.get(key))
