
import time
from functools import wraps


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Retry a function when a specified exception occurs."""

    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if delay < 0:
        raise ValueError("delay cannot be negative")

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return function(*args, **kwargs)

                except exceptions as error:
                    last_error = error

                    if attempt == max_attempts:
                        raise

                    time.sleep(delay)

            raise last_error

        return wrapper

    return decorator
