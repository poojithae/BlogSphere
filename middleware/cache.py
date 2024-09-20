import time
from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.utils.cache import (
    get_cache_key,
    get_max_age,
    has_vary_header,
    learn_cache_key,
    patch_response_headers,
)
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import parse_http_date_safe

class UpdateCacheMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
        self.cache_alias = settings.CACHE_MIDDLEWARE_ALIAS        
        self.page_timeout = None
        self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX

    @property
    def cache(self):
        return caches[self.cache_alias]

    def _should_update_cache(self, request, response):
        return hasattr(request, "_cache_update_cache") and request._cache_update_cache

    def process_response(self, request, response):
        if not self._should_update_cache(request, response):
            print("Cache not updated: request._cache_update_cache is False")
            return response

        if response.streaming or response.status_code not in (200, 304):
            return response

        if not request.COOKIES and response.cookies and has_vary_header(response, "Cookie"):
            return response

        if "private" in response.get("Cache-Control", ()):
            return response

        timeout = self.page_timeout or get_max_age(response) or self.cache_timeout
        if timeout == 0:
            return response

        patch_response_headers(response, timeout)
        if response.status_code == 200:
            cache_key = learn_cache_key(
                request, response, timeout, self.key_prefix, cache=self.cache
            )
            print(f"Caching response for key: {cache_key}")
            self.cache.set(cache_key, response, timeout)

        return response


class FetchFromCacheMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)
        self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        self.cache_alias = settings.CACHE_MIDDLEWARE_ALIAS

    @property
    def cache(self):
        return caches[self.cache_alias]

    def process_request(self, request):
        if request.method not in ("GET", "HEAD"):
            request._cache_update_cache = False
            return None

        cache_key = get_cache_key(request, self.key_prefix, "GET", cache=self.cache)
        if cache_key is None:
            print(f"No cache key available for request: {request.path}")
            request._cache_update_cache = True
            return None

        response = self.cache.get(cache_key)
        if response is None and request.method == "HEAD":
            cache_key = get_cache_key(
                request, self.key_prefix, "HEAD", cache=self.cache
            )
            response = self.cache.get(cache_key)

        if response is None:
            print("Cache miss for key: {cache_key}")
            request._cache_update_cache = True
            return None

        if (max_age_seconds := get_max_age(response)) is not None and (
            expires_timestamp := parse_http_date_safe(response["Expires"])
        ) is not None:
            now_timestamp = int(time.time())
            remaining_seconds = expires_timestamp - now_timestamp
            response["Age"] = max(0, max_age_seconds - remaining_seconds)

        request._cache_update_cache = False
        return response


class CacheMiddleware(UpdateCacheMiddleware, FetchFromCacheMiddleware):

    def __init__(self, get_response, cache_timeout=None, page_timeout=None, **kwargs):
        super().__init__(get_response)

        self.key_prefix = kwargs.get("key_prefix", settings.CACHE_MIDDLEWARE_KEY_PREFIX)
        self.cache_alias = kwargs.get("cache_alias", DEFAULT_CACHE_ALIAS)

        if cache_timeout is not None:
            self.cache_timeout = cache_timeout
        self.page_timeout = page_timeout
