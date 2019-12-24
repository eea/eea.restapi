from functools import wraps
from time import time

import logging


logger = logging.getLogger('eea.restapi')


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        logger.warning('func:%r args:[%r, %r] took: %2.4f sec' %
                       (f.__name__, args, kw, te - ts))

        return result

    return wrap
