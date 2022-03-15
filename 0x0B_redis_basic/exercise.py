#!/usr/bin/env python3
"""
Learning Redis Basic with python
"""
from functools import wraps
import redis
from typing import Union, Callable, Optional
import uuid


def count_calls(func: Callable) -> Callable:
    """
    Increments the count for that key every time the method is called
    and returns the value returned by the original method.
    """
    key = func.__qualname__

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper for decorator functionality
        """
        self._redis.incr(key)
        return func(self, *args, **kwargs)

    return wrapper


def call_history(func: Callable) -> Callable:
    """
    History of inputs and outputs for a particular function.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper for decorator functionality
        """
        input = str(args)
        self._redis.rpush(func.__qualname__ + ":inputs", input)

        output = str(func(self, *args, **kwargs))
        self._redis.rpush(func.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(fn: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = n_calls.decode('utf-8')
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{f_name}(*{i}) -> {o}')


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data and return the random key created
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        Retrieve data from cache and cnverts it to the desired format
        """
        result = self._redis.get(key)
        if fn:
            result = fn(result)
        return result

    def get_str(self, key: str) -> str:
        """
        Retrieve data from cache and cnverts it to string format
        """
        result = self._redis.get(key)
        result_converted = result.decode("utf-8")
        return result_converted

    def get_int(self, key: str) -> int:
        """
        Retrieve data from cache and converts it to int format
        """
        result = self._redis.get(key)
        try:
            result_converted = int(result.decode("utf-8"))
        except Exception:
            result_converted = 0
        return result_converted
