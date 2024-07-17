#!/usr/bin/env python3
"""
Web module
"""
from functools import wraps
from typing import Callable

import redis
import requests

r = redis.Redis()


def access_count(method: Callable) -> Callable:
    """"
    Increments the count associated with the URL in
    the Redis cache and calls the method with the URL and its arguments.
    """

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
    """
    Retrieves the content of a web page from the specified URL
    and caches it for a specified duration.
    Parameters:
        url (str): The URL of the web page to retrieve.
    Returns:
        str: The content of the web page.
    Raises:
        requests.exceptions.RequestException: If there is an
        error making the HTTP request.
    Side Effects:
        - Increments the access count for the specified URL
        in the Redis cache.
        - Caches the content of the web page for a specified
        duration in the Redis cache.
    """
    response = requests.get(url)
    return response.text
