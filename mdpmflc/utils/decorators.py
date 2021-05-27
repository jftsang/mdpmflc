from functools import wraps
import logging
from time import time

def timed(msg="", logger=logging.getLogger()):
    def decorator(f):
        @wraps(f)
        def decorated_f(*args, **kwargs):
            logger.info(f"Beginning {msg}...")
            tic = time()
            try:
                return f(*args, **kwargs)
            finally:
                toc = time()
                logger.info(f"Done {msg}. Time elapsed {toc-tic} s.")

        return decorated_f
    return decorator
