#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from typing import Any, Callable
from unittest import result 
import redis
import uuid


class Cache:
    """
    Create cache and store the data
    """
    def __init__(self) -> None:
        """
        Initialize the redis object and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """
        Store data and return the random key created
        """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key


    def get(self, key: str, fn: Callable) -> Any:
        """
        Retrieve data from cache and cnverts it to the desired format 
        """
        result = self._redis.get(key)
        if fn is not None:
            result = fn(result)
        return result

    def get_str(self, key: str) -> str:
        """
        Retrieve data from cache and cnverts it to string format 
        """
        result = self._redis.get(key)
        result_converted = str(result)
        return result_converted

    def get_int(self, key: str) -> int:
        """
        Retrieve data from cache and converts it to int format
        """
        result = self._redis.get(key)
        result_converted = int(result)
        return result_converted
        
