from diskcache import Cache

from mdpmflc import CACHEDIR
from mdpmflc.config import CACHE_LIMIT

mdpmflc_cache = Cache(
    directory=CACHEDIR,
    expire=3600,
    size_limit=CACHE_LIMIT,
    eviction_policy="least-recently-used",
)
