from functools import wraps
import logging
from inspect import signature
from time import time


def timed(msg="", log_fn=logging.info):
    """Display log messages before and after running the function, with
    the latter message displaying the elapsed time.

    For vectorized functions, you almost certainly want the decorators
    this way round:

        @timed()
        @np.vectorize
        def func(x):
            ...

        func(xs)

    to make sure that the logging only gets done once in all, rather
    than once for each x in xs.
    """
    def decorator(f):
        @wraps(f)
        def timed_f(*args, **kwargs):
            arguments = signature(f).bind(*args, **kwargs).arguments
            log_fn("Begin " + msg.format(**arguments))
            tic = time()
            try:
                return f(*args, **kwargs)
            finally:
                toc = time()
                log_fn("Done " + msg.format(**arguments) + f" in {toc - tic} s.")

        return timed_f
    return decorator


class Maybe:
    def __init__(self, *exc_classes):
        self.exc_classes = exc_classes

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as exc:
                if any(isinstance(exc, cls) for cls in self.exc_classes):
                    return None
                raise

        return wrapper
