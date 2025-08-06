# File: backend/cache/legendary_cache_manager.py
"""
⚡🎸 N3EXTPATH - LEGENDARY CACHE MANAGER 🎸⚡
Professional Redis caching system with Swiss precision performance
Built: 2025-08-05 17:13:09 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import json
import hashlib
import pickle
import gzip
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
import redis.asyncio as redis
from functools import wraps
import time
import logging

T = TypeVar('T')

class CacheStrategy(Enum):
    """Cache invalidation strategies"""
    TIME_BASED = "time_based"
    LRU = "lru"
    LFU = "lfu" 
    WRITE_THROUGH = "write_through"
    WRITE_BEHIND = "write_behind"
    LEGENDARY = "legendary"  # Special strategy for RICKROLL187

class CacheLevel(Enum):
    """Cache hierarchy levels"""
    L1_MEMORY = "l1_memory"      # In-memory cache
    L2_REDIS = "l2_redis"        # Redis cache
    L3_DATABASE = "l3_database"   # Database cache
    LEGENDARY_CACHE = "legendary_cache"  # Special cache for legendary data

@dataclass
class CacheConfig:
    """Cache configuration"""
    default_ttl: int = 3600  # 1 hour
    max_size: int = 10000
    compression: bool = True
    serialization: str = "json"  # json, pickle, msgpack
    strategy: CacheStrategy = CacheStrategy.TIME_BASED
    legendary_mode: bool = False

@dataclass
class CacheStats:
    """Cache statistics"""
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0
    memory_usage: int = 0
    legendary_hits: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0
    
    @property
    def legendary_hit_rate(self) -> float:
        return (self.legendary_hits / self.hits * 100) if self.hits > 0 else 0.0

class LegendaryCacheManager:
    """Professional Multi-Level Cache Manager with Swiss Precision"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/1", config: CacheConfig = None):
        self.config = config or CacheConfig()
        self.redis_client = None
        self.memory_cache: Dict[str, Any] = {}
        self.cache_stats = CacheStats()
        self.logger = logging.getLogger(__name__)
        
        # Cache key prefixes for organization
        self.key_prefixes = {
            "user_data": "usr:",
            "okr_data": "okr:",
            "performance_data": "perf:",
            "dashboard_data": "dash:",
            "api_response": "api:",
            "session_data": "sess:",
            "legendary_data": "legend:",  # Special prefix for RICKROLL187
            "system_cache": "sys:"
        }
        
        # Initialize Redis connection
        asyncio.create_task(self._initialize_redis(redis_url))
        
        # Start background tasks
        asyncio.create_task(self._cache_maintenance_task())
        asyncio.create_task(self._stats_collection_task())
    
    async def _initialize_redis(self, redis_url: str):
        """Initialize Redis connection with legendary configuration"""
        try:
            self.redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=False,  # We handle encoding ourselves
                max_connections=20,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis_client.ping()
            self.logger.info("🎸 Legendary Redis cache connection established! 🎸")
            
            # Set Redis configurations for legendary performance
            await self.redis_client.config_set("maxmemory-policy", "allkeys-lru")
            await self.redis_client.config_set("tcp-keepalive", "60")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            # Fallback to memory cache only
            self.redis_client = None
    
    def _generate_cache_key(self, prefix: str, key: str, user_id: str = None) -> str:
        """Generate cache key with legendary precision"""
        
        # Add user context if provided
        if user_id:
            # Special handling for RICKROLL187
            if user_id == "rickroll187":
                prefix = self.key_prefixes["legendary_data"]
            key = f"{key}:user:{user_id}"
        
        # Generate hash for long keys to avoid Redis key length limits
        if len(key) > 200:
            key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
            key = f"{key[:100]}:hash:{key_hash}"
        
        return f"{self.key_prefixes.get(prefix, prefix)}{key}"
    
    def _serialize_data(self, data: Any) -> bytes:
        """Serialize data with compression if enabled"""
        
        if self.config.serialization == "pickle":
            serialized = pickle.dumps(data)
        elif self.config.serialization == "json":
            serialized = json.dumps(data, default=str, ensure_ascii=False).encode('utf-8')
        else:
            # Default to JSON
            serialized = json.dumps(data, default=str, ensure_ascii=False).encode('utf-8')
        
        # Compress if enabled and data is large enough
        if self.config.compression and len(serialized) > 1024:
            serialized = gzip.compress(serialized)
        
        return serialized
    
    def _deserialize_data(self, data: bytes) -> Any:
        """Deserialize data with decompression if needed"""
        
        # Try decompression first
        try:
            if data.startswith(b'\x1f\x8b'):  # gzip magic number
                data = gzip.decompress(data)
        except:
            pass  # Not compressed or compression failed
        
        # Deserialize
        if self.config.serialization == "pickle":
            return pickle.loads(data)
        elif self.config.serialization == "json":
            return json.loads(data.decode('utf-8'))
        else:
            # Default to JSON
            return json.loads(data.decode('utf-8'))
    
    async def get(self, key: str, prefix: str = "system_cache", user_id: str = None, 
                  default: Any = None) -> Any:
        """Get value from cache with multi-level lookup"""
        
        cache_key = self._generate_cache_key(prefix, key, user_id)
        start_time = time.time()
        
        try:
            # L1 Cache: Memory (fastest)
            if cache_key in self.memory_cache:
                self.cache_stats.hits += 1
                if user_id == "rickroll187":
                    self.cache_stats.legendary_hits += 1
                
                lookup_time = (time.time() - start_time) * 1000
                self.logger.debug(f"L1 cache hit for {cache_key} in {lookup_time:.2f}ms")
                return self.memory_cache[cache_key]
            
            # L2 Cache: Redis (fast)
            if self.redis_client:
                cached_data = await self.redis_client.get(cache_key)
                if cached_data:
                    deserialized_data = self._deserialize_data(cached_data)
                    
                    # Store in L1 cache for next time
                    self._set_memory_cache(cache_key, deserialized_data)
                    
                    self.cache_stats.hits += 1
                    if user_id == "rickroll187":
                        self.cache_stats.legendary_hits += 1
                    
                    lookup_time = (time.time() - start_time) * 1000
                    self.logger.debug(f"L2 cache hit for {cache_key} in {lookup_time:.2f}ms")
                    return deserialized_data
            
            # Cache miss
            self.cache_stats.misses += 1
            lookup_time = (time.time() - start_time) * 1000
            self.logger.debug(f"Cache miss for {cache_key} in {lookup_time:.2f}ms")
            return default
            
        except Exception as e:
            self.logger.error(f"Cache get error for {cache_key}: {e}")
            self.cache_stats.misses += 1
            return default
    
    async def set(self, key: str, value: Any, ttl: int = None, prefix: str = "system_cache", 
                  user_id: str = None) -> bool:
        """Set value in cache with multi-level storage"""
        
        cache_key = self._generate_cache_key(prefix, key, user_id)
        ttl = ttl or self.config.default_ttl
        
        # Special TTL for legendary data
        if user_id == "rickroll187":
            ttl = ttl * 2  # Legendary data stays cached longer
        
        start_time = time.time()
        
        try:
            # L1 Cache: Memory
            self._set_memory_cache(cache_key, value)
            
            # L2 Cache: Redis
            if self.redis_client:
                serialized_data = self._serialize_data(value)
                await self.redis_client.setex(cache_key, ttl, serialized_data)
            
            self.cache_stats.sets += 1
            
            storage_time = (time.time() - start_time) * 1000
            self.logger.debug(f"Cached {cache_key} in {storage_time:.2f}ms (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            self.logger.error(f"Cache set error for {cache_key}: {e}")
            return False
    
    def _set_memory_cache(self, key: str, value: Any):
        """Set value in memory cache with size management"""
        
        # Check memory cache size
        if len(self.memory_cache) >= self.config.max_size:
            # Evict oldest entries (simple FIFO for now)
            oldest_keys = list(self.memory_cache.keys())[:len(self.memory_cache) // 10]
            for old_key in oldest_keys:
                del self.memory_cache[old_key]
                self.cache_stats.evictions += 1
        
        self.memory_cache[key] = value
    
    async def delete(self, key: str, prefix: str = "system_cache", user_id: str = None) -> bool:
        """Delete value from all cache levels"""
        
        cache_key = self._generate_cache_key(prefix, key, user_id)
        
        try:
            # Delete from L1 cache
            if cache_key in self.memory_cache:
                del self.memory_cache[cache_key]
            
            # Delete from L2 cache
            if self.redis_client:
                await self.redis_client.delete(cache_key)
            
            self.cache_stats.deletes += 1
            self.logger.debug(f"Deleted cache key: {cache_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Cache delete error for {cache_key}: {e}")
            return False
    
    async def exists(self, key: str, prefix: str = "system_cache", user_id: str = None) -> bool:
        """Check if key exists in cache"""
        
        cache_key = self._generate_cache_key(prefix, key, user_id)
        
        # Check L1 cache first
        if cache_key in self.memory_cache:
            return True
        
        # Check L2 cache
        if self.redis_client:
            return bool(await self.redis_client.exists(cache_key))
        
        return False
    
    async def increment(self, key: str, amount: int = 1, prefix: str = "system_cache", 
                       user_id: str = None, ttl: int = None) -> int:
        """Increment numeric value in cache"""
        
        cache_key = self._generate_cache_key(prefix, key, user_id)
        ttl = ttl or self.config.default_ttl
        
        try:
            if self.redis_client:
                # Use Redis atomic increment
                new_value = await self.redis_client.incr(cache_key, amount)
                await self.redis_client.expire(cache_key, ttl)
                
                # Update memory cache
                self.memory_cache[cache_key] = new_value
                
                return new_value
            else:
                # Fallback to memory cache
                current_value = self.memory_cache.get(cache_key, 0)
                new_value = current_value + amount
                self.memory_cache[cache_key] = new_value
                return new_value
                
        except Exception as e:
            self.logger.error(f"Cache increment error for {cache_key}: {e}")
            return 0
    
    async def get_multiple(self, keys: List[str], prefix: str = "system_cache", 
                          user_id: str = None) -> Dict[str, Any]:
        """Get multiple values from cache efficiently"""
        
        cache_keys = [self._generate_cache_key(prefix, key, user_id) for key in keys]
        results = {}
        
        try:
            # Check L1 cache first
            missing_keys = []
            for i, cache_key in enumerate(cache_keys):
                if cache_key in self.memory_cache:
                    results[keys[i]] = self.memory_cache[cache_key]
                    self.cache_stats.hits += 1
                else:
                    missing_keys.append((i, cache_key))
            
            # Get missing keys from Redis
            if missing_keys and self.redis_client:
                redis_keys = [cache_key for _, cache_key in missing_keys]
                redis_values = await self.redis_client.mget(redis_keys)
                
                for (i, cache_key), value in zip(missing_keys, redis_values):
                    if value:
                        deserialized_value = self._deserialize_data(value)
                        results[keys[i]] = deserialized_value
                        # Cache in L1 for next time
                        self._set_memory_cache(cache_key, deserialized_value)
                        self.cache_stats.hits += 1
                    else:
                        self.cache_stats.misses += 1
            else:
                # All missing keys are cache misses
                self.cache_stats.misses += len(missing_keys)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Cache get_multiple error: {e}")
            return {}
    
    async def set_multiple(self, data: Dict[str, Any], ttl: int = None, 
                          prefix: str = "system_cache", user_id: str = None) -> bool:
        """Set multiple values in cache efficiently"""
        
        ttl = ttl or self.config.default_ttl
        
        try:
            # Set in L1 cache
            for key, value in data.items():
                cache_key = self._generate_cache_key(prefix, key, user_id)
                self._set_memory_cache(cache_key, value)
            
            # Set in Redis using pipeline
            if self.redis_client:
                pipe = self.redis_client.pipeline()
                for key, value in data.items():
                    cache_key = self._generate_cache_key(prefix, key, user_id)
                    serialized_data = self._serialize_data(value)
                    pipe.setex(cache_key, ttl, serialized_data)
                
                await pipe.execute()
            
            self.cache_stats.sets += len(data)
            return True
            
        except Exception as e:
            self.logger.error(f"Cache set_multiple error: {e}")
            return False
    
    async def flush_prefix(self, prefix: str, user_id: str = None) -> int:
        """Flush all keys with given prefix"""
        
        if prefix in self.key_prefixes:
            redis_prefix = self.key_prefixes[prefix]
        else:
            redis_prefix = prefix
        
        if user_id:
            redis_prefix += f"*:user:{user_id}"
        else:
            redis_prefix += "*"
        
        deleted_count = 0
        
        try:
            # Delete from L1 cache
            keys_to_delete = [k for k in self.memory_cache.keys() if k.startswith(redis_prefix)]
            for key in keys_to_delete:
                del self.memory_cache[key]
                deleted_count += 1
            
            # Delete from Redis
            if self.redis_client:
                cursor = 0
                while True:
                    cursor, keys = await self.redis_client.scan(cursor, match=redis_prefix, count=100)
                    if keys:
                        await self.redis_client.delete(*keys)
                        deleted_count += len(keys)
                    if cursor == 0:
                        break
            
            self.logger.info(f"Flushed {deleted_count} keys with prefix: {redis_prefix}")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Cache flush_prefix error for {redis_prefix}: {e}")
            return 0
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        
        memory_usage = sum(len(str(v)) for v in self.memory_cache.values())
        
        redis_info = {}
        if self.redis_client:
            try:
                redis_info = await self.redis_client.info('memory')
            except:
                redis_info = {"error": "Could not fetch Redis info"}
        
        return {
            "cache_stats": {
                "hits": self.cache_stats.hits,
                "misses": self.cache_stats.misses,
                "hit_rate": round(self.cache_stats.hit_rate, 2),
                "sets": self.cache_stats.sets,
                "deletes": self.cache_stats.deletes,
                "evictions": self.cache_stats.evictions,
                "legendary_hits": self.cache_stats.legendary_hits,
                "legendary_hit_rate": round(self.cache_stats.legendary_hit_rate, 2)
            },
            "memory_cache": {
                "size": len(self.memory_cache),
                "max_size": self.config.max_size,
                "usage_bytes": memory_usage,
                "usage_percentage": round(len(self.memory_cache) / self.config.max_size * 100, 2)
            },
            "redis_info": redis_info,
            "configuration": {
                "default_ttl": self.config.default_ttl,
                "compression": self.config.compression,
                "serialization": self.config.serialization,
                "strategy": self.config.strategy.value,
                "legendary_mode": self.config.legendary_mode
            },
            "legendary_message": "🎸 Cache performance is legendary! Swiss precision caching active! 🎸" if self.cache_stats.legendary_hits > 0 else None
        }
    
    async def _cache_maintenance_task(self):
        """Background cache maintenance with Swiss precision"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                
                # Clean up expired entries from memory cache
                # (Redis handles its own expiration)
                current_size = len(self.memory_cache)
                
                # If memory cache is getting too large, do aggressive cleanup
                if current_size > self.config.max_size * 0.8:
                    # Remove 20% of entries (oldest first)
                    keys_to_remove = list(self.memory_cache.keys())[:int(current_size * 0.2)]
                    for key in keys_to_remove:
                        del self.memory_cache[key]
                        self.cache_stats.evictions += 1
                    
                    self.logger.info(f"Cache maintenance: removed {len(keys_to_remove)} entries")
                
            except Exception as e:
                self.logger.error(f"Cache maintenance error: {e}")
    
    async def _stats_collection_task(self):
        """Background stats collection"""
        
        while True:
            try:
                await asyncio.sleep(60)  # Collect stats every minute
                
                # Log cache performance if we have significant activity
                if self.cache_stats.hits + self.cache_stats.misses > 100:
                    hit_rate = self.cache_stats.hit_rate
                    if hit_rate < 50:
                        self.logger.warning(f"Low cache hit rate: {hit_rate:.1f}%")
                    elif hit_rate > 90:
                        self.logger.info(f"🎸 Excellent cache performance: {hit_rate:.1f}% hit rate! 🎸")
                
            except Exception as e:
                self.logger.error(f"Stats collection error: {e}")

# Caching decorators for easy use
def cache_result(ttl: int = 3600, prefix: str = "api_response", 
                key_generator: Callable = None, use_user_context: bool = True):
    """Decorator to cache function results"""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_generator:
                cache_key = key_generator(*args, **kwargs)
            else:
                # Default key generation
                func_name = func.__name__
                args_str = "_".join(str(arg) for arg in args[:3])  # First 3 args
                kwargs_str = "_".join(f"{k}:{v}" for k, v in sorted(kwargs.items())[:3])
                cache_key = f"{func_name}_{args_str}_{kwargs_str}"
            
            # Extract user context if needed
            user_id = None
            if use_user_context:
                # Try to find user_id in kwargs or args
                if 'user_id' in kwargs:
                    user_id = kwargs['user_id']
                elif 'current_user' in kwargs and hasattr(kwargs['current_user'], 'user_id'):
                    user_id = kwargs['current_user'].user_id
            
            # Try to get from cache
            cached_result = await legendary_cache_manager.get(
                cache_key, prefix=prefix, user_id=user_id
            )
            
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            
            await legendary_cache_manager.set(
                cache_key, result, ttl=ttl, prefix=prefix, user_id=user_id
            )
            
            return result
        
        return wrapper
    return decorator

# Global cache manager instance
legendary_cache_manager = LegendaryCacheManager()
