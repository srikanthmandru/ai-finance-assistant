from cachetools import TTLCache


class CacheManager:
    def __init__(self, ttl_seconds: int = 1800, maxsize: int = 100):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl_seconds)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value