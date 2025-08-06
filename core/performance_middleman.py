"""
⚡🎸 N3EXTPATH - LEGENDARY PERFORMANCE OPTIMIZATION MIDDLEWARE 🎸⚡
More optimized than Swiss precision engineering with legendary performance mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 LEGENDARY PERFORMANCE CHAMPION EDITION! 🏆
Current Time: 2025-08-04 15:15:45 UTC - WE'RE OPTIMIZING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

import time
import asyncio
import psutil
import logging
from typing import Dict, Any, Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading

# Set up legendary logging
logger = logging.getLogger(__name__)

class LegendaryPerformanceTracker:
    """
    ⚡ THE LEGENDARY PERFORMANCE TRACKING SYSTEM! ⚡
    More precise than Swiss chronometers with code bro optimization! 🎸🏃
    """
    
    def __init__(self):
        self.request_metrics = defaultdict(list)
        self.response_times = deque(maxlen=1000)  # Keep last 1000 requests
        self.error_counts = defaultdict(int)
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
            'avg_time': 0.0
        })
        self.legendary_jokes = [
            "Why is our API so fast? Because RICKROLL187 optimized it at 15:15:45 UTC! ⚡🎸",
            "What's faster than Swiss precision? Our legendary performance monitoring! 🏃",
            "Why don't code bros worry about performance? Because we optimize like legends! 💪",
            "What do you call sub-millisecond response times? A RICKROLL187 special! 🎸⚡"
        ]
        self.lock = threading.Lock()
    
    def track_request(self, endpoint: str, response_time: float, status_code: int):
        """
        Track legendary request performance!
        More accurate than Swiss timing with code bro precision! ⚡📊
        """
        with self.lock:
            # Update response times
            self.response_times.append(response_time)
            
            # Update endpoint statistics
            stats = self.endpoint_stats[endpoint]
            stats['count'] += 1
            stats['total_time'] += response_time
            stats['min_time'] = min(stats['min_time'], response_time)
            stats['max_time'] = max(stats['max_time'], response_time)
            stats['avg_time'] = stats['total_time'] / stats['count']
            
            # Track errors
            if status_code >= 400:
                self.error_counts[status_code] += 1
            
            # Store detailed metrics
            self.request_metrics[endpoint].append({
                'timestamp': datetime.utcnow().isoformat(),
                'response_time': response_time,
                'status_code': status_code
            })
            
            # Keep only last 100 requests per endpoint
            if len(self.request_metrics[endpoint]) > 100:
                self.request_metrics[endpoint] = self.request_metrics[endpoint][-100:]
    
    def get_legendary_performance_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive legendary performance statistics!
        More insightful than Swiss analytics with code bro intelligence! 📊🎸
        """
        import random
        
        with self.lock:
            if not self.response_times:
                return {
                    "status": "No performance data yet - Start making requests! 🚀",
                    "legendary_joke": random.choice(self.legendary_jokes)
                }
            
            # Calculate overall statistics
            avg_response_time = sum(self.response_times) / len(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
            
            # Get system metrics
            system_stats = self.get_system_metrics()
            
            return {
                "performance_overview": {
                    "timestamp": "2025-08-04 15:15:45 UTC",
                    "monitored_by": "RICKROLL187 - The Legendary Performance Master 🎸",
                    "total_requests": len(self.response_times),
                    "avg_response_time_ms": round(avg_response_time * 1000, 2),
                    "min_response_time_ms": round(min_response_time * 1000, 2),
                    "max_response_time_ms": round(max_response_time * 1000, 2),
                    "performance_grade": self.calculate_performance_grade(avg_response_time),
                    "legendary_factor": "MAXIMUM OPTIMIZATION! ⚡🏆"
                },
                "endpoint_statistics": dict(self.endpoint_stats),
                "error_statistics": dict(self.error_counts),
                "system_metrics": system_stats,
                "performance_tips": [
                    "🚀 Average response time under 100ms = LEGENDARY!",
                    "⚡ Optimized by RICKROLL187 with Swiss precision!",
                    "🎸 Code bros always optimize for maximum performance!",
                    "🏆 Sub-millisecond responses = Ultimate legendary status!"
                ],
                "legendary_joke": random.choice(self.legendary_jokes),
                "optimization_status": "PERFECTLY OPTIMIZED BY RICKROLL187 AT 15:15:45 UTC! 🎸⚡"
            }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Get legendary system performance metrics!
        More comprehensive than Swiss diagnostics with code bro monitoring! 🖥️⚡
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage_percent": round(cpu_percent, 2),
                "memory_usage_percent": round(memory.percent, 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_usage_percent": round(disk.percent, 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "system_health": "LEGENDARY PERFORMANCE! 🖥️⚡" if cpu_percent < 80 and memory.percent < 80 else "OPTIMIZING... 🔧",
                "rickroll187_optimization": "SWISS PRECISION SYSTEM MONITORING! 🎸🔧"
            }
        except Exception as e:
            logger.warning(f"System metrics error: {e}")
            return {
                "status": "System metrics unavailable",
                "legendary_note": "Still running with legendary performance! 🎸"
            }
    
    def calculate_performance_grade(self, avg_response_time: float) -> str:
        """
        Calculate legendary performance grade!
        More grading than Swiss educational precision with code bro standards! 📝⚡
        """
        ms_time = avg_response_time * 1000
        
        if ms_time < 10:
            return "A++ LEGENDARY RICKROLL187 LEVEL! 🏆⚡"
        elif ms_time < 50:
            return "A+ SWISS PRECISION EXCELLENT! 🎯"
        elif ms_time < 100:
            return "A CODE BRO APPROVED! 🎸"
        elif ms_time < 200:
            return "B+ GOOD PERFORMANCE! 👍"
        elif ms_time < 500:
            return "B ACCEPTABLE PERFORMANCE 📊"
        else:
            return "C NEEDS LEGENDARY OPTIMIZATION! 🔧"

# Global legendary performance tracker
legendary_performance_tracker = LegendaryPerformanceTracker()

class LegendaryPerformanceMiddleware:
    """
    ⚡ LEGENDARY PERFORMANCE OPTIMIZATION MIDDLEWARE! ⚡
    More optimized than Swiss watches with code bro efficiency! 🎸🏃
    """
    
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 300  # 5 minutes TTL
        self.compression_enabled = True
        
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with legendary performance optimization!
        Faster than RICKROLL187's guitar solos with Swiss precision! ⚡🎸
        """
        start_time = time.time()
        endpoint = f"{request.method} {request.url.path}"
        
        # Check cache for GET requests
        if request.method == "GET":
            cached_response = self.get_cached_response(str(request.url))
            if cached_response:
                processing_time = time.time() - start_time
                legendary_performance_tracker.track_request(endpoint, processing_time, 200)
                
                # Add cache headers
                response = JSONResponse(content=cached_response)
                response.headers["X-Legendary-Cache"] = "HIT"
                response.headers["X-Cache-Time"] = f"{processing_time:.3f}s"
                response.headers["X-Optimized-By"] = "RICKROLL187"
                
                return response
        
        # Process request
        response = await call_next(request)
        processing_time = time.time() - start_time
        
        # Track performance
        legendary_performance_tracker.track_request(
            endpoint, processing_time, response.status_code
        )
        
        # Cache successful GET responses
        if request.method == "GET" and response.status_code == 200:
            try:
                if hasattr(response, 'body'):
                    response_body = response.body.decode()
                    self.cache_response(str(request.url), json.loads(response_body))
            except Exception as e:
                logger.debug(f"Cache error: {e}")
        
        # Add performance headers
        response.headers["X-Response-Time"] = f"{processing_time:.3f}s"
        response.headers["X-Performance-Grade"] = legendary_performance_tracker.calculate_performance_grade(processing_time)
        response.headers["X-Legendary-Optimization"] = "RICKROLL187 PERFORMANCE BOOST! ⚡"
        
        return response
    
    def get_cached_response(self, cache_key: str) -> Any:
        """Get cached response if available and not expired!"""
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
            else:
                # Remove expired cache
                del self.cache[cache_key]
        return None
    
    def cache_response(self, cache_key: str, response_data: Any):
        """Cache response data with timestamp!"""
        self.cache[cache_key] = (response_data, time.time())
        
        # Simple cache cleanup - remove oldest entries if cache gets too large
        if len(self.cache) > 1000:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]

# Global legendary performance middleware instance
legendary_performance_middleware = LegendaryPerformanceMiddleware()

async def legendary_performance_monitor_endpoint(request: Request) -> Dict[str, Any]:
    """
    Get legendary performance monitoring dashboard!
    More insightful than Swiss intelligence with code bro analytics! 📊🎸
    """
    return legendary_performance_tracker.get_legendary_performance_stats()

# Performance optimization utilities
class LegendaryOptimizationUtils:
    """
    🔧 LEGENDARY OPTIMIZATION UTILITIES! 🔧
    More efficient than Swiss engineering with code bro optimization! 🎸⚡
    """
    
    @staticmethod
    def optimize_database_query(query_func):
        """Decorator for database query optimization!"""
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await query_func(*args, **kwargs)
            query_time = time.time() - start_time
            
            if query_time > 0.1:  # Log slow queries
                logger.warning(f"Slow query detected: {query_func.__name__} took {query_time:.3f}s")
            
            return result
        return wrapper
    
    @staticmethod
    def legendary_cache_result(ttl: int = 300):
        """Decorator for result caching with TTL!"""
        cache = {}
        
        def decorator(func):
            async def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
                
                if cache_key in cache:
                    result, timestamp = cache[cache_key]
                    if time.time() - timestamp < ttl:
                        return result
                
                result = await func(*args, **kwargs)
                cache[cache_key] = (result, time.time())
                
                return result
            return wrapper
        return decorator

if __name__ == "__main__":
    print("⚡🎸 N3EXTPATH LEGENDARY PERFORMANCE MIDDLEWARE LOADED! 🎸⚡")
    print("🏆 LEGENDARY PERFORMANCE CHAMPION EDITION! 🏆")
    print(f"⏰ Optimization Time: 2025-08-04 15:15:45 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🚀 PERFORMANCE OPTIMIZED BY RICKROLL187 WITH SWISS PRECISION! 🚀")
