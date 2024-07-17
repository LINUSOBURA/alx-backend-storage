#!/usr/bin/env python3
"""
Web module
"""
from functools import wraps
from typing import Callable

import redis
import requests
import requests

r = redis.Redis()


def access_count(method: Callable) -> Callable:

    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        r.incr(f"count:{url}")
        return method(url, *args, **kwargs)

    return wrapper


def cache_result(expiration: int = 10) -> Callable:

    def decorator(method: Callable) -> Callable:

        @wraps(method)
        def wrapper(url: str, *args, **kwargs):
            cached = r.get(f"cache:{url}")
            if cached:
                return cached.decode("utf-8")

            content = method(url, *args, **kwargs)
            r.setex(f"cache:{url}", expiration, content)
            return content

        return wrapper

    return decorator


@access_count
@cache_result(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
