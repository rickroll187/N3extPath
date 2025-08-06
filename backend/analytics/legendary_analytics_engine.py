# File: backend/analytics/legendary_analytics_engine.py
"""
📊🎸 N3EXTPATH - LEGENDARY ANALYTICS ENGINE 🎸📊
Professional real-time analytics and metrics collection
Built: 2025-08-05 15:56:54 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
import uuid

@dataclass
class MetricPoint:
    """Individual metric data point"""
    timestamp: datetime
    metric_name: str
    value: float
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class AnalyticsEvent:
    """Analytics event with context"""
    event_id: str
    event_type: str
    user_id: str
    timestamp: datetime
    properties: Dict[str, Any] = field(default_factory=dict)
    session_id: Optional[str] = None

class LegendaryAnalyticsEngine:
    """Professional Real-Time Analytics Engine"""
    
    def __init__(self):
        self.metrics_buffer = defaultdict(lambda: deque(maxlen=1000))
        self.events_buffer = deque(maxlen=5000)
        self.active_sessions = {}
        self.real_time_stats = {
            "total_users": 0,
            "active_sessions": 0,
            "requests_per_minute": 0,
            "average_response_time": 0.0,
            "error_rate": 0.0,
            "legendary_actions": 0
        }
        
        # Start background analytics processing
        asyncio.create_task(self._process_analytics_loop())
    
    async def track_event(self, event_type: str, user_id: str, properties: Dict[str, Any] = None) -> str:
        """Track analytics event with legendary precision"""
        event_id = str(uuid.uuid4())
        
        event = AnalyticsEvent(
            event_id=event_id,
            event_type=event_type,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            properties=properties or {},
            session_id=self.active_sessions.get(user_id, {}).get("session_id")
        )
        
        self.events_buffer.append(event)
        
        # Special handling for RICKROLL187 events
        if user_id == "rickroll187":
            event.properties["legendary_status"] = True
            event.properties["founder_action"] = True
            self.real_time_stats["legendary_actions"] += 1
        
        # Update real-time stats
        await self._update_real_time_stats(event)
        
        return event_id
    
    async def record_metric(self, metric_name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record performance metric with Swiss precision"""
        metric = MetricPoint(
            timestamp=datetime.utcnow(),
            metric_name=metric_name,
            value=value,
            tags=tags or {},
            metadata={"recorded_by": "legendary_analytics_engine"}
        )
        
        self.metrics_buffer[metric_name].append(metric)
        
        # Update aggregated stats
        if metric_name == "response_time_ms":
            await self._update_response_time_stats(value)
        elif metric_name == "request_count":
            await self._update_request_stats()
        elif metric_name == "error_count":
            await self._update_error_stats()
    
    async def start_user_session(self, user_id: str, user_agent: str = None, ip_address: str = None) -> str:
        """Start user session tracking"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "start_time": datetime.utcnow(),
            "user_agent": user_agent,
            "ip_address": ip_address,
            "page_views": 0,
            "actions": 0,
            "is_legendary": user_id == "rickroll187"
        }
        
        self.active_sessions[user_id] = session_data
        self.real_time_stats["active_sessions"] = len(self.active_sessions)
        
        # Track session start event
        await self.track_event("session_start", user_id, {
            "session_id": session_id,
            "user_agent": user_agent,
            "is_legendary_user": user_id == "rickroll187"
        })
        
        return session_id
    
    async def end_user_session(self, user_id: str) -> None:
        """End user session tracking"""
        if user_id in self.active_sessions:
            session_data = self.active_sessions[user_id]
            session_duration = (datetime.utcnow() - session_data["start_time"]).total_seconds()
            
            # Track session end event
            await self.track_event("session_end", user_id, {
                "session_id": session_data["session_id"],
                "duration_seconds": session_duration,
                "page_views": session_data["page_views"],
                "actions": session_data["actions"]
            })
            
            del self.active_sessions[user_id]
            self.real_time_stats["active_sessions"] = len(self.active_sessions)
    
    async def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time analytics dashboard data"""
        
        # Calculate time-based metrics
        current_time = datetime.utcnow()
        last_hour = current_time - timedelta(hours=1)
        last_day = current_time - timedelta(days=1)
        
        # Get recent events
        recent_events = [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp.isoformat(),
                "properties": event.properties,
                "is_legendary": event.user_id == "rickroll187"
            }
            for event in list(self.events_buffer)[-50:]  # Last 50 events
        ]
        
        # Get performance metrics
        response_times = list(self.metrics_buffer.get("response_time_ms", []))
        recent_response_times = [m.value for m in response_times if m.timestamp > last_hour]
        
        # Calculate user activity
        unique_users_last_hour = len(set(
            event.user_id for event in self.events_buffer 
            if event.timestamp > last_hour
        ))
        
        # Get legendary user activity
        legendary_events = [
            event for event in self.events_buffer 
            if event.user_id == "rickroll187" and event.timestamp > last_day
        ]
        
        dashboard_data = {
            "current_time": current_time.isoformat(),
            "real_time_stats": self.real_time_stats.copy(),
            "performance_metrics": {
                "average_response_time": sum(recent_response_times) / len(recent_response_times) if recent_response_times else 0,
                "requests_last_hour": len(recent_response_times),
                "p95_response_time": self._calculate_percentile(recent_response_times, 95) if recent_response_times else 0,
                "p99_response_time": self._calculate_percentile(recent_response_times, 99) if recent_response_times else 0
            },
            "user_activity": {
                "active_sessions": len(self.active_sessions),
                "unique_users_last_hour": unique_users_last_hour,
                "total_events_last_hour": len([e for e in self.events_buffer if e.timestamp > last_hour]),
                "legendary_user_active": "rickroll187" in self.active_sessions
            },
            "legendary_metrics": {
                "rickroll187_events_today": len(legendary_events),
                "legendary_actions_total": self.real_time_stats["legendary_actions"],
                "legendary_session_active": "rickroll187" in self.active_sessions,
                "legendary_last_activity": legendary_events[-1].timestamp.isoformat() if legendary_events else None
            },
            "recent_events": recent_events,
            "top_event_types": self._get_top_event_types(last_hour),
            "system_health": {
                "uptime_seconds": time.time() - getattr(self, '_start_time', time.time()),
                "memory_usage_percent": self._get_memory_usage(),
                "legendary_status": "🎸 OPERATIONAL WITH SWISS PRECISION 🎸"
            }
        }
        
        return dashboard_data
    
    async def get_user_analytics(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get analytics for specific user"""
        start_date = datetime.utcnow() - timedelta(days=days_back)
        
        user_events = [
            event for event in self.events_buffer 
            if event.user_id == user_id and event.timestamp > start_date
        ]
        
        # Group events by type
        event_types = defaultdict(int)
        daily_activity = defaultdict(int)
        
        for event in user_events:
            event_types[event.event_type] += 1
            day_key = event.timestamp.strftime("%Y-%m-%d")
            daily_activity[day_key] += 1
        
        # Special analytics for RICKROLL187
        if user_id == "rickroll187":
            legendary_stats = {
                "legendary_actions": len([e for e in user_events if e.properties.get("legendary_status")]),
                "founder_privileges_used": len([e for e in user_events if e.properties.get("founder_action")]),
                "swiss_precision_events": len([e for e in user_events if "precision" in str(e.properties)]),
                "code_bro_interactions": len([e for e in user_events if "code_bro" in str(e.properties).lower()])
            }
        else:
            legendary_stats = {}
        
        return {
            "user_id": user_id,
            "analysis_period_days": days_back,
            "total_events": len(user_events),
            "event_types": dict(event_types),
            "daily_activity": dict(daily_activity),
            "average_daily_events": len(user_events) / days_back if days_back > 0 else 0,
            "most_active_day": max(daily_activity.items(), key=lambda x: x[1]) if daily_activity else None,
            "legendary_stats": legendary_stats,
            "is_legendary_user": user_id == "rickroll187"
        }
    
    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile with legendary precision"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int((percentile / 100) * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _get_top_event_types(self, since: datetime) -> List[Dict[str, Any]]:
        """Get top event types since given time"""
        event_counts = defaultdict(int)
        
        for event in self.events_buffer:
            if event.timestamp > since:
                event_counts[event.event_type] += 1
        
        return [
            {"event_type": event_type, "count": count}
            for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
    
    def _get_memory_usage(self) -> float:
        """Get memory usage percentage (mock implementation)"""
        # In real implementation, would use psutil or similar
        return 42.0  # Legendary number
    
    async def _update_real_time_stats(self, event: AnalyticsEvent) -> None:
        """Update real-time statistics"""
        if event.event_type == "page_view":
            if event.user_id in self.active_sessions:
                self.active_sessions[event.user_id]["page_views"] += 1
        
        if event.event_type in ["login", "session_start"]:
            self.real_time_stats["total_users"] = len(set(e.user_id for e in self.events_buffer))
    
    async def _update_response_time_stats(self, response_time: float) -> None:
        """Update response time statistics"""
        recent_times = [
            m.value for m in list(self.metrics_buffer["response_time_ms"])[-100:]
        ]
        
        if recent_times:
            self.real_time_stats["average_response_time"] = sum(recent_times) / len(recent_times)
    
    async def _update_request_stats(self) -> None:
        """Update request statistics"""
        current_time = datetime.utcnow()
        last_minute = current_time - timedelta(minutes=1)
        
        recent_requests = [
            m for m in self.metrics_buffer["request_count"]
            if m.timestamp > last_minute
        ]
        
        self.real_time_stats["requests_per_minute"] = len(recent_requests)
    
    async def _update_error_stats(self) -> None:
        """Update error rate statistics"""
        current_time = datetime.utcnow()
        last_hour = current_time - timedelta(hours=1)
        
        recent_requests = len([
            m for m in self.metrics_buffer["request_count"]
            if m.timestamp > last_hour
        ])
        
        recent_errors = len([
            m for m in self.metrics_buffer["error_count"]
            if m.timestamp > last_hour
        ])
        
        if recent_requests > 0:
            self.real_time_stats["error_rate"] = (recent_errors / recent_requests) * 100
    
    async def _process_analytics_loop(self) -> None:
        """Background processing loop for analytics"""
        self._start_time = time.time()
        
        while True:
            try:
                # Process any queued analytics
                await self._cleanup_old_data()
                await self._generate_insights()
                
                # Sleep for legendary precision timing
                await asyncio.sleep(60)  # Process every minute
                
            except Exception as e:
                print(f"Analytics processing error: {e}")
                await asyncio.sleep(30)  # Retry in 30 seconds
    
    async def _cleanup_old_data(self) -> None:
        """Clean up old analytics data"""
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        # Clean old events
        self.events_buffer = deque([
            event for event in self.events_buffer 
            if event.timestamp > cutoff_time
        ], maxlen=5000)
        
        # Clean old metrics
        for metric_name in self.metrics_buffer:
            self.metrics_buffer[metric_name] = deque([
                metric for metric in self.metrics_buffer[metric_name]
                if metric.timestamp > cutoff_time
            ], maxlen=1000)
    
    async def _generate_insights(self) -> None:
        """Generate analytical insights"""
        # This would contain ML-based insights in production
        current_time = datetime.utcnow()
        
        if current_time.minute == 0:  # Every hour
            print(f"🎸 Legendary Analytics Insight: {len(self.events_buffer)} events processed! 🎸")
            print(f"🎸 RICKROLL187 legendary actions: {self.real_time_stats['legendary_actions']} 🎸")

# Global analytics engine instance
legendary_analytics = LegendaryAnalyticsEngine()
