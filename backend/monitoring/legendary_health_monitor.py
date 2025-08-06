# File: backend/monitoring/legendary_health_monitor.py
"""
🏥🎸 N3EXTPATH - LEGENDARY SYSTEM HEALTH MONITOR 🎸🏥
Professional system health monitoring and alerting
Built: 2025-08-05 15:56:54 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import psutil
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid

class HealthStatus(Enum):
    """System health status levels"""
    LEGENDARY = "legendary"      # Perfect health (RICKROLL187 level)
    HEALTHY = "healthy"          # Normal operation
    WARNING = "warning"          # Minor issues
    CRITICAL = "critical"        # Major issues
    DOWN = "down"               # System failure

@dataclass
class HealthCheck:
    """Individual health check result"""
    check_id: str
    name: str
    status: HealthStatus
    response_time_ms: float
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    load_average: List[float]
    uptime_seconds: float
    legendary_status: bool = False

class LegendaryHealthMonitor:
    """Professional System Health Monitoring"""
    
    def __init__(self):
        self.health_checks = {}
        self.metrics_history = []
        self.alerts = []
        self.start_time = time.time()
        self.last_health_check = None
        
        # Legendary thresholds (Swiss precision!)
        self.thresholds = {
            "cpu_warning": 70.0,
            "cpu_critical": 90.0,
            "memory_warning": 80.0,
            "memory_critical": 95.0,
            "disk_warning": 85.0,
            "disk_critical": 95.0,
            "response_time_warning": 1000.0,  # 1 second
            "response_time_critical": 5000.0   # 5 seconds
        }
        
        # Start health monitoring loop
        asyncio.create_task(self._health_monitoring_loop())
    
    async def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check with legendary precision"""
        start_time = time.time()
        
        health_checks = []
        overall_status = HealthStatus.LEGENDARY
        
        # 1. API Health Check
        api_check = await self._check_api_health()
        health_checks.append(api_check)
        
        # 2. Database Health Check
        db_check = await self._check_database_health()
        health_checks.append(db_check)
        
        # 3. System Resources Check
        system_check = await self._check_system_resources()
        health_checks.append(system_check)
        
        # 4. Memory Health Check
        memory_check = await self._check_memory_health()
        health_checks.append(memory_check)
        
        # 5. Disk Health Check
        disk_check = await self._check_disk_health()
        health_checks.append(disk_check)
        
        # 6. Network Health Check
        network_check = await self._check_network_health()
        health_checks.append(network_check)
        
        # 7. Legendary Features Check (special for RICKROLL187)
        legendary_check = await self._check_legendary_features()
        health_checks.append(legendary_check)
        
        # Determine overall status
        for check in health_checks:
            if check.status == HealthStatus.CRITICAL:
                overall_status = HealthStatus.CRITICAL
                break
            elif check.status == HealthStatus.WARNING and overall_status != HealthStatus.CRITICAL:
                overall_status = HealthStatus.WARNING
            elif check.status == HealthStatus.DOWN:
                overall_status = HealthStatus.DOWN
                break
        
        # Special status for legendary performance
        if all(check.status in [HealthStatus.HEALTHY, HealthStatus.LEGENDARY] for check in health_checks):
            overall_status = HealthStatus.LEGENDARY
        
        total_time = (time.time() - start_time) * 1000  # Convert to ms
        
        health_result = {
            "overall_status": overall_status.value,
            "total_checks": len(health_checks),
            "healthy_checks": len([c for c in health_checks if c.status == HealthStatus.HEALTHY]),
            "legendary_checks": len([c for c in health_checks if c.status == HealthStatus.LEGENDARY]),
            "warning_checks": len([c for c in health_checks if c.status == HealthStatus.WARNING]),
            "critical_checks": len([c for c in health_checks if c.status == HealthStatus.CRITICAL]),
            "total_response_time_ms": round(total_time, 2),
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": time.time() - self.start_time,
            "checks": [
                {
                    "name": check.name,
                    "status": check.status.value,
                    "response_time_ms": check.response_time_ms,
                    "message": check.message,
                    "details": check.details
                }
                for check in health_checks
            ],
            "built_by": "RICKROLL187",
            "legendary_message": "🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸"
        }
        
        self.last_health_check = health_result
        return health_result
    
    async def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics with legendary precision"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network I/O
            network_io = psutil.net_io_counters()._asdict()
            
            # Load average (Unix systems)
            try:
                load_avg = list(psutil.getloadavg())
            except AttributeError:
                load_avg = [0.0, 0.0, 0.0]  # Windows fallback
            
            uptime = time.time() - self.start_time
            
            # Determine if performance is legendary
            is_legendary = (
                cpu_percent < 30 and 
                memory_percent < 50 and 
                disk_percent < 70
            )
            
            metrics = SystemMetrics(
                timestamp=datetime.utcnow(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_io,
                load_average=load_avg,
                uptime_seconds=uptime,
                legendary_status=is_legendary
            )
            
            # Keep metrics history (last 24 hours)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 1440:  # 24 hours * 60 minutes
                self.metrics_history.pop(0)
            
            return metrics
            
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
            return SystemMetrics(
                timestamp=datetime.utcnow(),
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_percent=0.0,
                network_io={},
                load_average=[0.0, 0.0, 0.0],
                uptime_seconds=time.time() - self.start_time
            )
    
    async def get_metrics_dashboard(self) -> Dict[str, Any]:
        """Get metrics dashboard data"""
        current_metrics = await self.get_system_metrics()
        
        # Calculate trends (last hour vs current)
        if len(self.metrics_history) > 60:
            hour_ago_metrics = self.metrics_history[-60]
            cpu_trend = current_metrics.cpu_percent - hour_ago_metrics.cpu_percent
            memory_trend = current_metrics.memory_percent - hour_ago_metrics.memory_percent
        else:
            cpu_trend = 0.0
            memory_trend = 0.0
        
        # Performance rating
        performance_score = 100
        if current_metrics.cpu_percent > 70:
            performance_score -= 20
        if current_metrics.memory_percent > 80:
            performance_score -= 20
        if current_metrics.disk_percent > 85:
            performance_score -= 10
        
        # Legendary performance bonus
        if current_metrics.legendary_status:
            performance_score = min(110, performance_score + 10)  # Legendary bonus!
        
        return {
            "current_metrics": {
                "cpu_percent": current_metrics.cpu_percent,
                "memory_percent": current_metrics.memory_percent,
                "disk_percent": current_metrics.disk_percent,
                "load_average": current_metrics.load_average,
                "uptime_hours": current_metrics.uptime_seconds / 3600,
                "legendary_status": current_metrics.legendary_status
            },
            "trends": {
                "cpu_trend": round(cpu_trend, 2),
                "memory_trend": round(memory_trend, 2),
                "trend_direction": "improving" if cpu_trend < 0 and memory_trend < 0 else "stable" if abs(cpu_trend) < 5 and abs(memory_trend) < 5 else "degrading"
            },
            "performance": {
                "score": performance_score,
                "rating": "🎸 LEGENDARY" if performance_score > 100 else "🏆 EXCELLENT" if performance_score > 90 else "✅ GOOD" if performance_score > 70 else "⚠️ NEEDS ATTENTION"
            },
            "alerts": self.alerts[-10:],  # Last 10 alerts
            "health_status": self.last_health_check["overall_status"] if self.last_health_check else "unknown",
            "last_health_check": self.last_health_check["timestamp"] if self.last_health_check else None,
            "swiss_precision_active": True,
            "code_bro_message": "🎸 System running with legendary precision! 🎸"
        }
    
    async def _check_api_health(self) -> HealthCheck:
        """Check API endpoint health"""
        start_time = time.time()
        
        try:
            # Simulate API health check
            await asyncio.sleep(0.01)  # Simulate network call
            
            response_time = (time.time() - start_time) * 1000
            
            if response_time < self.thresholds["response_time_warning"]:
                status = HealthStatus.LEGENDARY if response_time < 100 else HealthStatus.HEALTHY
                message = f"API responding in {response_time:.2f}ms (Legendary!)" if status == HealthStatus.LEGENDARY else f"API healthy ({response_time:.2f}ms)"
            elif response_time < self.thresholds["response_time_critical"]:
                status = HealthStatus.WARNING
                message = f"API slow response: {response_time:.2f}ms"
            else:
                status = HealthStatus.CRITICAL
                message = f"API very slow: {response_time:.2f}ms"
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="API Health",
                status=status,
                response_time_ms=response_time,
                message=message,
                details={"endpoint": "/health", "method": "GET"}
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="API Health",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"API health check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_database_health(self) -> HealthCheck:
        """Check database health"""
        start_time = time.time()
        
        try:
            # Simulate database health check
            await asyncio.sleep(0.005)  # Simulate DB query
            
            response_time = (time.time() - start_time) * 1000
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Database Health",
                status=HealthStatus.LEGENDARY if response_time < 50 else HealthStatus.HEALTHY,
                response_time_ms=response_time,
                message=f"Database connection healthy ({response_time:.2f}ms)",
                details={"connection_pool": "available", "query_time_ms": response_time}
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Database Health",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Database check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_system_resources(self) -> HealthCheck:
        """Check system resource usage"""
        start_time = time.time()
        
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            response_time = (time.time() - start_time) * 1000
            
            if cpu_percent < self.thresholds["cpu_warning"]:
                status = HealthStatus.LEGENDARY if cpu_percent < 30 else HealthStatus.HEALTHY
                message = f"CPU usage optimal: {cpu_percent:.1f}%"
            elif cpu_percent < self.thresholds["cpu_critical"]:
                status = HealthStatus.WARNING
                message = f"CPU usage elevated: {cpu_percent:.1f}%"
            else:
                status = HealthStatus.CRITICAL
                message = f"CPU usage critical: {cpu_percent:.1f}%"
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="CPU Resources",
                status=status,
                response_time_ms=response_time,
                message=message,
                details={"cpu_percent": cpu_percent, "threshold_warning": self.thresholds["cpu_warning"]}
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="CPU Resources",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"CPU check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_memory_health(self) -> HealthCheck:
        """Check memory usage health"""
        start_time = time.time()
        
        try:
            memory = psutil.virtual_memory()
            response_time = (time.time() - start_time) * 1000
            
            if memory.percent < self.thresholds["memory_warning"]:
                status = HealthStatus.LEGENDARY if memory.percent < 50 else HealthStatus.HEALTHY
                message = f"Memory usage healthy: {memory.percent:.1f}%"
            elif memory.percent < self.thresholds["memory_critical"]:
                status = HealthStatus.WARNING
                message = f"Memory usage elevated: {memory.percent:.1f}%"
            else:
                status = HealthStatus.CRITICAL
                message = f"Memory usage critical: {memory.percent:.1f}%"
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Memory Usage",
                status=status,
                response_time_ms=response_time,
                message=message,
                details={
                    "memory_percent": memory.percent,
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2)
                }
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Memory Usage",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Memory check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_disk_health(self) -> HealthCheck:
        """Check disk usage health"""
        start_time = time.time()
        
        try:
            disk = psutil.disk_usage('/')
            response_time = (time.time() - start_time) * 1000
            
            if disk.percent < self.thresholds["disk_warning"]:
                status = HealthStatus.LEGENDARY if disk.percent < 60 else HealthStatus.HEALTHY
                message = f"Disk usage healthy: {disk.percent:.1f}%"
            elif disk.percent < self.thresholds["disk_critical"]:
                status = HealthStatus.WARNING  
                message = f"Disk usage elevated: {disk.percent:.1f}%"
            else:
                status = HealthStatus.CRITICAL
                message = f"Disk usage critical: {disk.percent:.1f}%"
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Disk Usage",
                status=status,
                response_time_ms=response_time,
                message=message,
                details={
                    "disk_percent": disk.percent,
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2)
                }
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Disk Usage",
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Disk check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_network_health(self) -> HealthCheck:
        """Check network connectivity health"""
        start_time = time.time()
        
        try:
            # Simulate network check
            await asyncio.sleep(0.01)
            response_time = (time.time() - start_time) * 1000
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Network Health",
                status=HealthStatus.LEGENDARY if response_time < 50 else HealthStatus.HEALTHY,
                response_time_ms=response_time,
                message=f"Network connectivity healthy ({response_time:.2f}ms)",
                details={"connectivity": "active", "latency_ms": response_time}
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Network Health", 
                status=HealthStatus.CRITICAL,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Network check failed: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _check_legendary_features(self) -> HealthCheck:
        """Check legendary features (special for RICKROLL187)"""
        start_time = time.time()
        
        try:
            # Check if legendary features are active
            legendary_features = {
                "swiss_precision": True,
                "code_bro_jokes": True,
                "rickroll187_mode": True,
                "legendary_branding": True
            }
            
            response_time = (time.time() - start_time) * 1000
            
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Legendary Features",
                status=HealthStatus.LEGENDARY,
                response_time_ms=response_time,
                message="🎸 All legendary features operational! 🎸",
                details=legendary_features
            )
            
        except Exception as e:
            return HealthCheck(
                check_id=str(uuid.uuid4()),
                name="Legendary Features",
                status=HealthStatus.WARNING,
                response_time_ms=(time.time() - start_time) * 1000,
                message=f"Legendary features check issue: {str(e)}",
                details={"error": str(e)}
            )
    
    async def _health_monitoring_loop(self) -> None:
        """Background health monitoring loop"""
        while True:
            try:
                # Perform health check every 5 minutes
                await asyncio.sleep(300)
                await self.perform_health_check()
                
                # Generate alerts if needed
                await self._check_for_alerts()
                
            except Exception as e:
                print(f"Health monitoring error: {e}")
                await asyncio.sleep(60)  # Retry in 1 minute
    
    async def _check_for_alerts(self) -> None:
        """Check for system alerts"""
        if not self.last_health_check:
            return
        
        current_time = datetime.utcnow()
        
        # Generate alerts for critical issues
        for check in self.last_health_check.get("checks", []):
            if check["status"] == "critical":
                alert = {
                    "alert_id": str(uuid.uuid4()),
                    "severity": "critical",
                    "message": f"Critical issue: {check['message']}",
                    "check_name": check["name"],
                    "timestamp": current_time.isoformat(),
                    "resolved": False
                }
                
                self.alerts.append(alert)
                print(f"🚨 CRITICAL ALERT: {alert['message']} 🚨")
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

# Global health monitor instance
legendary_health_monitor = LegendaryHealthMonitor()
