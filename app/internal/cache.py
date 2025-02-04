import time
from typing import Callable, Any
from functools import wraps


class CustomCache:
    def __init__(self, expiry_seconds: int = 60, max_size: int | None = None) -> None:
        self.expiry_seconds = expiry_seconds
        self.max_size = max_size
        self.cache_store: dict[str, tuple] = {}
        
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = await self._generate_cache_key(func, args, kwargs)
            cached_result = await self._get_cached_data(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = await func(*args, **kwargs)
            await self._store_cached_data(cache_key, result)
            return result
        
        return wrapper
    
    async def _generate_cache_key(self, func: Callable, args: tuple, kwargs: dict) -> str:
        arg_string = ":".join(str(arg) for arg in args)
        kwarg_string = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{func.__name__}:{arg_string}:{kwarg_string}"
    
    async def _get_cached_data(self, cache_key: str) -> Any | None:
        if cache_key in self.cache_store:
            result, timestamp = self.cache_store[cache_key]
            if time.time() - timestamp < self.expiry_seconds:
                return result
            else:
                del self.cache_store[cache_key]
        return None
    
    async def _store_cached_data(self, cache_key:str, result: Any) -> None:
        if self.max_size and len(self.cache_store) >= self.max_size:
            oldest_key = min(self.cache_store.items(), key=lambda x: x[1][1])[0]
            del self.cache_store[oldest_key]
        self.cache_store[cache_key] = (result, time.time())