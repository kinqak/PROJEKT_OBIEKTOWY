from functools import wraps
import time

# dekorator logujący czas pobierania danych
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start

        if args and hasattr(args[0], "download_time"):
            args[0].download_time = elapsed

        return result
    return wrapper