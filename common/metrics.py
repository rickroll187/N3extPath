"""
Prometheus Metrics Utilities
Because you can't improve what you don't measure, bro!
"""
import os
import time
from prometheus_client import Counter, Histogram, Gauge, Info
from functools import wraps

# Global metrics - because sharing is caring
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['service', 'method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['service', 'method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections_total',
    'Number of active connections',
    ['service']
)

HR_EVENTS = Counter(
    'hr_events_total',
    'Total HR events processed',
    ['service', 'event_type', 'status']
)

SERVICE_INFO = Info(
    'n3xtpath_service_info',
    'N3xtPath service information'
)

class MetricsBro:
    """Your friendly neighborhood metrics collector"""
    
    def __init__(self, service_name: str = None):
        self.service_name = service_name or os.getenv('SERVICE_NAME', 'unknown')
        
        # Set service info
        SERVICE_INFO.info({
            'service': self.service_name,
            'version': '1.0.0',
            'built_by': 'rickroll187',
            'built_at': '2025-08-03T14:48:32Z'
        })
    
    def track_request(self, method: str, endpoint: str, status_code: int):
        """Track HTTP requests like a monitoring ninja"""
        REQUEST_COUNT.labels(
            service=self.service_name,
            method=method,
            endpoint=endpoint,
            status=str(status_code)
        ).inc()
    
    def track_hr_event(self, event_type: str, status: str = 'success'):
        """Track HR-specific events"""
        HR_EVENTS.labels(
            service=self.service_name,
            event_type=event_type,
            status=status
        ).inc()
    
    def set_active_connections(self, count: int):
        """Set the number of active connections"""
        ACTIVE_CONNECTIONS.labels(service=self.service_name).set(count)

def metrics_middleware(service_name: str = None):
    """Middleware decorator for automatic metrics collection"""
    metrics = MetricsBro(service_name)
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            request = args[0] if args else None
            
            try:
                response = await func(*args, **kwargs)
                status_code = getattr(response, 'status_code', 200)
                
                # Track the request
                if request:
                    metrics.track_request(
                        method=request.method,
                        endpoint=request.url.path,
                        status_code=status_code
                    )
                
                # Track duration
                duration = time.time() - start_time
                REQUEST_DURATION.labels(
                    service=metrics.service_name,
                    method=request.method if request else 'unknown',
                    endpoint=request.url.path if request else 'unknown'
                ).observe(duration)
                
                return response
            except Exception as e:
                # Track error
                if request:
                    metrics.track_request(
                        method=request.method,
                        endpoint=request.url.path,
                        status_code=500
                    )
                raise e
        
        return wrapper
    return decorator

def get_metrics_instance(service_name: str = None) -> MetricsBro:
    """Factory function for metrics instance"""
    return MetricsBro(service_name)
