# File: backend/performance/legendary_performance_monitor.py
"""
📊🎸 N3EXTPATH - LEGENDARY PERFORMANCE MONITOR 🎸📊
Professional performance monitoring and optimization system
Built: 2025-08-05 17:13:09 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import time
import psutil
import gc
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Callable, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import deque, defaultdict, Counter
import redis
import json
import threading
from contextlib import asynccontextmanager, contextmanager
import logging

class MetricType(Enum):
    """Performance metric types"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DATABASE_QUERY_TIME = "db_query_time"
    CACHE_HIT_RATE = "cache_hit_rate"
    CONCURRENT_USERS = "concurrent_users"
    LEGENDARY_METRICS = "legendary_metrics"

class AlertLevel(Enum):
    """Performance alert levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    LEGENDARY = "legendary"  # For RICKROLL187 alerts

@dataclass
class PerformanceMetric:
    """Individual performance metric"""
    metric_type: MetricType
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceAlert:
    """Performance alert"""
    alert_id: str
    level: AlertLevel
    metric_type: MetricType
    message: str
    current_value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False
    legendary_alert: bool = False

class RequestMetrics(NamedTuple):
    """HTTP request metrics"""
    path: str
    method: str
    status_code: int
    response_time: float
    user_id: Optional[str]
    is_legendary: bool = False

class LegendaryPerformanceMonitor:
    """Professional Performance Monitoring System with Swiss Precision"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        self.logger = logging.getLogger(__name__)
        
        # Metric storage (in-memory circular buffers)
        self.metrics_buffer = defaultdict(lambda: deque(maxlen=1000))
        self.request_metrics = deque(maxlen=10000)
        self.alerts = deque(maxlen=100)
        
        # Performance thresholds
        self.thresholds = {
            MetricType.RESPONSE_TIME: {"warning": 1.0, "critical": 5.0},  # seconds
            MetricType.ERROR_RATE: {"warning": 5.0, "critical": 10.0},    # percentage
            MetricType.CPU_USAGE: {"warning": 70.0, "critical": 90.0},    # percentage
            MetricType.MEMORY_USAGE: {"warning": 80.0, "critical": 95.0}, # percentage
            MetricType.CACHE_HIT_RATE: {"warning": 70.0, "critical": 50.0}, # percentage (inverse)
            MetricType.CONCURRENT_USERS: {"warning": 1000, "critical": 1500}
        }
        
        # Legendary performance tracking
        self.legendary_metrics = {
            "rickroll187_requests": 0,
            "legendary_response_times": deque(maxlen=100),
            "swiss_precision_score": 100.0,
            "code_bro_interactions": 0
        }
        
        # Start background monitoring
        asyncio.create_task(self._system_monitoring_loop())
        asyncio.create_task(self._metrics_aggregation_loop())
        asyncio.create_task(self._alert_processing_loop())
    
    def record_request(self, path: str, method: str, status_code: int, 
                      response_time: float, user_id: str = None):
        """Record HTTP request metrics"""
        
        is_legendary = user_id == "rickroll187"
        
        # Create request metric
        metric = RequestMetrics(
            path=path,
            method=method,
            status_code=status_code,
            response_time=response_time,
            user_id=user_id,
            is_legendary=is_legendary
        )
        
        self.request_metrics.append(metric)
        
        # Update legendary metrics
        if is_legendary:
            self.legendary_metrics["rickroll187_requests"] += 1
            self.legendary_metrics["legendary_response_times"].append(response_time)
            
            # Update Swiss precision score based on response time
            if response_time < 0.1:  # Under 100ms
                self.legendary_metrics["swiss_precision_score"] = min(
                    self.legendary_metrics["swiss_precision_score"] + 0.1, 100.0
                )
            elif response_time > 1.0:  # Over 1 second
                self.legendary_metrics["swiss_precision_score"] = max(
                    self.legendary_metrics["swiss_precision_score"] - 1.0, 0.0
                )
        
        # Record performance metrics
        asyncio.create_task(self._record_metric(
            MetricType.RESPONSE_TIME,
            response_time,
            tags={"path": path, "method": method, "user_type": "legendary" if is_legendary else "standard"}
        ))
        
        # Check for performance alerts
        if response_time > self.thresholds[MetricType.RESPONSE_TIME]["critical"]:
            asyncio.create_task(self._create_alert(
                AlertLevel.LEGENDARY if is_legendary else AlertLevel.CRITICAL,
                MetricType.RESPONSE_TIME,
                f"{'Legendary user' if is_legendary else 'Request'} response time exceeded critical threshold",
                response_time,
                self.thresholds[MetricType.RESPONSE_TIME]["critical"]
            ))
    
    async def _record_metric(self, metric_type: MetricType, value: float, 
                           tags: Dict[str, str] = None, metadata: Dict[str, Any] = None):
        """Record performance metric"""
        
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            timestamp=datetime.now(timezone.utc),
            tags=tags or {},
            metadata=metadata or {}
        )
        
        # Store in memory buffer
        self.metrics_buffer[metric_type].append(metric)
        
        # Store in Redis for persistence
        try:
            metric_key = f"performance_metric:{metric_type.value}:{int(time.time())}"
            metric_data = {
                "value": value,
                "timestamp": metric.timestamp.isoformat(),
                "tags": json.dumps(tags or {}),
                "metadata": json.dumps(metadata or {})
            }
            
            self.redis_client.hset(metric_key, mapping=metric_data)
            self.redis_client.expire(metric_key, 86400 * 7)  # Keep for 7 days
            
            # Add to time series
            ts_key = f"ts:performance:{metric_type.value}"
            self.redis_client.zadd(ts_key, {metric_key: metric.timestamp.timestamp()})
            self.redis_client.expire(ts_key, 86400 * 7)
            
        except Exception as e:
            self.logger.error(f"Failed to store metric: {e}")
    
    async def _create_alert(self, level: AlertLevel, metric_type: MetricType, 
                          message: str, current_value: float, threshold: float):
        """Create performance alert"""
        
        alert = PerformanceAlert(
            alert_id=f"alert_{int(time.time())}_{metric_type.value}",
            level=level,
            metric_type=metric_type,
            message=message,
            current_value=current_value,
            threshold=threshold,
            timestamp=datetime.now(timezone.utc),
            legendary_alert=level == AlertLevel.LEGENDARY
        )
        
        self.alerts.append(alert)
        
        # Log alert
        log_message = f"Performance Alert [{level.value.upper()}]: {message} (Value: {current_value}, Threshold: {threshold})"
        if level == AlertLevel.LEGENDARY:
            self.logger.warning(f"🎸 LEGENDARY ALERT: {log_message} 🎸")
        else:
            self.logger.warning(log_message)
        
        # Store alert in Redis
        try:
            alert_key = f"performance_alert:{alert.alert_id}"
            alert_data = {
                "level": level.value,
                "metric_type": metric_type.value,
                "message": message,
                "current_value": current_value,
                "threshold": threshold,
                "timestamp": alert.timestamp.isoformat(),
                "resolved": "false",
                "legendary_alert": str(alert.legendary_alert)
            }
            
            self.redis_client.hset(alert_key, mapping=alert_data)
            self.redis_client.expire(alert_key, 86400 * 30)  # Keep for 30 days
            
        except Exception as e:
            self.logger.error(f"Failed to store alert: {e}")
    
    @asynccontextmanager
    async def measure_async(self, operation_name: str, tags: Dict[str, str] = None):
        """Async context manager to measure operation performance"""
        
        start_time = time.time()
        start_memory = psutil.virtual_memory().percent
        
        try:
            yield
        finally:
            end_time = time.time()
            end_memory = psutil.virtual_memory().percent
            
            duration = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Record metrics
            await self._record_metric(
                MetricType.RESPONSE_TIME,
                duration,
                tags={**(tags or {}), "operation": operation_name}
            )
            
            if abs(memory_delta) > 1.0:  # Significant memory change
                await self._record_metric(
                    MetricType.MEMORY_USAGE,
                    memory_delta,
                    tags={**(tags or {}), "operation": operation_name, "type": "delta"}
                )
    
    @contextmanager
    def measure_sync(self, operation_name: str, tags: Dict[str, str] = None):
        """Sync context manager to measure operation performance"""
        
        start_time = time.time()
        
        try:
            yield
        finally:
            duration = time.time() - start_time
            
            # Create async task to record metric
            asyncio.create_task(self._record_metric(
                MetricType.RESPONSE_TIME,
                duration,
                tags={**(tags or {}), "operation": operation_name}
            ))
    
    def get_performance_summary(self, timeframe_minutes: int = 60) -> Dict[str, Any]:
        """Get performance summary for the last N minutes"""
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=timeframe_minutes)
        
        # Filter recent request metrics
        recent_requests = [
            req for req in self.request_metrics 
            if req.response_time > 0  # Basic validation
        ][-1000:]  # Last 1000 requests max
        
        if not recent_requests:
            return {"error": "No recent request data available"}
        
        # Calculate basic stats
        response_times = [req.response_time for req in recent_requests]
        error_requests = [req for req in recent_requests if req.status_code >= 400]
        legendary_requests = [req for req in recent_requests if req.is_legendary]
        
        # Performance calculations
        avg_response_time = statistics.mean(response_times) if response_times else 0
        median_response_time = statistics.median(response_times) if response_times else 0
        p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else 0
        p99_response_time = statistics.quantiles(response_times, n=100)[98] if len(response_times) > 100 else 0
        
        error_rate = (len(error_requests) / len(recent_requests)) * 100 if recent_requests else 0
        
        # Throughput (requests per minute)
        throughput = len(recent_requests) / timeframe_minutes if timeframe_minutes > 0 else 0
        
        # Most popular endpoints
        endpoint_counter = Counter(f"{req.method} {req.path}" for req in recent_requests)
        top_endpoints = endpoint_counter.most_common(10)
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Legendary metrics
        legendary_stats = {
            "rickroll187_requests": self.legendary_metrics["rickroll187_requests"],
            "legendary_request_percentage": (len(legendary_requests) / len(recent_requests)) * 100 if recent_requests else 0,
            "swiss_precision_score": self.legendary_metrics["swiss_precision_score"],
            "legendary_avg_response_time": statistics.mean([req.response_time for req in legendary_requests]) if legendary_requests else 0
        }
        
        return {
            "timeframe_minutes": timeframe_minutes,
            "total_requests": len(recent_requests),
            "performance_metrics": {
                "avg_response_time": round(avg_response_time, 3),
                "median_response_time": round(median_response_time, 3),
                "p95_response_time": round(p95_response_time, 3),
                "p99_response_time": round(p99_response_time, 3),
                "error_rate": round(error_rate, 2),
                "throughput_rpm": round(throughput, 2)
            },
            "system_metrics": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2)
            },
            "legendary_metrics": legendary_stats,
            "top_endpoints": [{"endpoint": endpoint, "count": count} for endpoint, count in top_endpoints],
            "recent_alerts": [
                {
                    "level": alert.level.value,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "legendary": alert.legendary_alert
                }
                for alert in list(self.alerts)[-5:]  # Last 5 alerts
            ],
            "performance_grade": self._calculate_performance_grade(avg_response_time, error_rate, cpu_percent),
            "legendary_message": "🎸 Performance monitoring with Swiss precision! 🎸" if legendary_requests else None
        }
    
    def _calculate_performance_grade(self, avg_response_time: float, error_rate: float, cpu_percent: float) -> str:
        """Calculate overall performance grade"""
        
        score = 100
        
        # Response time scoring
        if avg_response_time > 2.0:
            score -= 30
        elif avg_response_time > 1.0:
            score -= 15
        elif avg_response_time > 0.5:
            score -= 5
        
        # Error rate scoring
        if error_rate > 10:
            score -= 25
        elif error_rate > 5:
            score -= 15
        elif error_rate > 1:
            score -= 5
        
        # CPU usage scoring
        if cpu_percent > 90:
            score -= 20
        elif cpu_percent > 70:
            score -= 10
        elif cpu_percent > 50:
            score -= 5
        
        # Grade assignment
        if score >= 95:
            return "🎸 LEGENDARY (A+)"
        elif score >= 90:
            return "🏆 EXCELLENT (A)"
        elif score >= 80:
            return "✅ GOOD (B)"
        elif score >= 70:
            return "⚠️ FAIR (C)"
        elif score >= 60:
            return "🔴 POOR (D)"
        else:
            return "🚨 CRITICAL (F)"
    
    async def _system_monitoring_loop(self):
        """Background system monitoring loop"""
        
        while True:
            try:
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Record metrics
                await self._record_metric(MetricType.CPU_USAGE, cpu_percent)
                await self._record_metric(MetricType.MEMORY_USAGE, memory.percent)
                
                # Check for alerts
                if cpu_percent > self.thresholds[MetricType.CPU_USAGE]["critical"]:
                    await self._create_alert(
                        AlertLevel.CRITICAL,
                        MetricType.CPU_USAGE,
                        f"CPU usage critical: {cpu_percent:.1f}%",
                        cpu_percent,
                        self.thresholds[MetricType.CPU_USAGE]["critical"]
                    )
                
                if memory.percent > self.thresholds[MetricType.MEMORY_USAGE]["critical"]:
                    await self._create_alert(
                        AlertLevel.CRITICAL,
                        MetricType.MEMORY_USAGE,
                        f"Memory usage critical: {memory.percent:.1f}%",
                        memory.percent,
                        self.thresholds[MetricType.MEMORY_USAGE]["critical"]
                    )
                
                # Force garbage collection if memory is high
                if memory.percent > 85:
                    gc.collect()
                
            except Exception as e:
                self.logger.error(f"System monitoring error: {e}")
    
    async def _metrics_aggregation_loop(self):
        """Background metrics aggregation loop"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Aggregate every 5 minutes
                
                # Calculate aggregated metrics
                current_time = datetime.now(timezone.utc)
                
                # Recent request metrics (last 5 minutes)
                recent_requests = [
                    req for req in self.request_metrics
                    if req.response_time > 0  # Basic validation
                ][-500:]  # Last 500 requests
                
                if recent_requests:
                    # Calculate throughput
                    throughput = len(recent_requests) / 5  # requests per minute
                    await self._record_metric(MetricType.THROUGHPUT, throughput)
                    
                    # Calculate error rate
                    error_count = len([req for req in recent_requests if req.status_code >= 400])
                    error_rate = (error_count / len(recent_requests)) * 100
                    await self._record_metric(MetricType.ERROR_RATE, error_rate)
                    
                    # Update legendary metrics
                    legendary_count = len([req for req in recent_requests if req.is_legendary])
                    if legendary_count > 0:
                        self.legendary_metrics["code_bro_interactions"] += legendary_count
                
            except Exception as e:
                self.logger.error(f"Metrics aggregation error: {e}")
    
    async def _alert_processing_loop(self):
        """Background alert processing loop"""
        
        while True:
            try:
                await asyncio.sleep(60)  # Process alerts every minute
                
                # Check for alert resolution
                current_time = datetime.now(timezone.utc)
                
                for alert in self.alerts:
                    if not alert.resolved and (current_time - alert.timestamp).total_seconds() > 300:
                        # Check if condition has improved
                        if await self._check_alert_resolution(alert):
                            alert.resolved = True  # This doesn't work with NamedTuple, need to fix
                            
                            self.logger.info(f"Alert resolved: {alert.message}")
                
            except Exception as e:
                self.logger.error(f"Alert processing error: {e}")
    
    async def _check_alert_resolution(self, alert: PerformanceAlert) -> bool:
        """Check if alert condition has been resolved"""
        
        # Get recent metrics for the alert type
        recent_metrics = list(self.metrics_buffer[alert.metric_type])[-10:]  # Last 10 metrics
        
        if not recent_metrics:
            return False
        
        # Check if recent values are below threshold
        recent_values = [m.value for m in recent_metrics]
        avg_recent = statistics.mean(recent_values)
        
        # Different logic for different metric types
        if alert.metric_type in [MetricType.RESPONSE_TIME, MetricType.ERROR_RATE, 
                                MetricType.CPU_USAGE, MetricType.MEMORY_USAGE]:
            return avg_recent < alert.threshold * 0.8  # 80% of threshold
        elif alert.metric_type == MetricType.CACHE_HIT_RATE:
            return avg_recent > alert.threshold * 1.2  # 120% of threshold (inverse)
        
        return False

# Global performance monitor instance
legendary_performance_monitor = LegendaryPerformanceMonitor()

# Performance monitoring middleware for FastAPI
async def performance_monitoring_middleware(request, call_next):
    """FastAPI middleware for performance monitoring"""
    
    start_time = time.time()
    
    # Extract user info if available
    user_id = None
    if hasattr(request.state, 'user') and request.state.user:
        user_id = request.state.user.user_id
    
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        raise e
    finally:
        # Record metrics
        response_time = time.time() - start_time
        
        legendary_performance_monitor.record_request(
            path=request.url.path,
            method=request.method,
            status_code=status_code,
            response_time=response_time,
            user_id=user_id
        )
    
    return response
