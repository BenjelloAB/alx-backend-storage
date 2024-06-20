#!/usr/bin/env python3
""" Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()
'''The module-level Redis instance
'''


def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = redis_.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        redis_.incr(count_key)
        redis_.set(cached_key, html)
        redis_.expire(cached_key, 10)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    '''Method that Returns the content of a URL after
    caching the request's response and tracking the request
    '''
    req = requests.get(url)
    return req.text
