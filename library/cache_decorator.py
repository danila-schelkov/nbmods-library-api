import time
from typing import Callable


def time_cache(expire_seconds: float) -> Callable:
    cache = {}

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()

            if key in cache:
                value, timestamp = cache[key]
                if current_time - timestamp < expire_seconds:
                    return value

            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result

        return wrapper

    return decorator
