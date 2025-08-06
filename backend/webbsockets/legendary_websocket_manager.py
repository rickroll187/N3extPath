# File: backend/websockets/legendary_websocket_manager.py
"""
🌐🎸 N3EXTPATH - LEGENDARY WEBSOCKET MANAGER 🎸🌐
Professional real-time communication system with Swiss precision
Built: 2025-08-05 17:01:56 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
import redis
from fastapi import WebSocket, WebSocketDisconnect
import logging
from collections import defaultdict

class MessageType(Enum):
    """WebSocket message types"""
    CHAT = "chat"
    NOTIFICATION = "notification"
    PERFORMANCE_UPDATE = "performance_update"
    OKR_UPDATE = "okr_update"
    SYSTEM_ALERT = "system_alert"
    USER_STATUS = "user_status"
    TYPING_INDICATOR = "typing_indicator"
    LEGENDARY_ANNOUNCEMENT = "legendary_announcement"
    CODE_BRO_JOKE = "code_bro_joke"
    SWISS_PRECISION_UPDATE = "swiss_precision_update"

class UserStatus(Enum):
    """User online status"""
    ONLINE = "online"
    AWAY = "away"
    BUSY = "busy"
    OFFLINE = "offline"
    LEGENDARY = "legendary"  # Special status for RICKROLL187

@dataclass
class WebSocketConnection:
    """WebSocket connection information"""
    websocket: WebSocket
    user_id: str
    username: str
    connection_id: str
    connected_at: datetime
    last_activity: datetime
    is_legendary: bool = False
    status: UserStatus = UserStatus.ONLINE
    subscribed_channels: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WebSocketMessage:
    """WebSocket message structure"""
    message_id: str
    message_type: MessageType
    sender_id: str
    sender_username: str
    content: Any
    channel: Optional[str] = None
    recipients: Optional[List[str]] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_legendary: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

class LegendaryWebSocketManager:
    """Professional WebSocket Manager with Real-Time Capabilities"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.connections: Dict[str, WebSocketConnection] = {}
        self.user_connections: Dict[str, List[str]] = defaultdict(list)
        self.channel_subscriptions: Dict[str, Set[str]] = defaultdict(set)
        self.message_handlers: Dict[MessageType, List[Callable]] = defaultdict(list)
        
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        self.logger = logging.getLogger(__name__)
        
        # Initialize legendary channels
        self._initialize_legendary_channels()
        
        # Start background tasks
        asyncio.create_task(self._heartbeat_task())
        asyncio.create_task(self._cleanup_task())
    
    def _initialize_legendary_channels(self):
        """Initialize legendary communication channels"""
        legendary_channels = [
            "general",
            "announcements", 
            "performance_updates",
            "okr_updates",
            "system_alerts",
            "legendary_founder_channel",  # Special channel for RICKROLL187
            "code_bro_jokes",
            "swiss_precision_updates"
        ]
        
        for channel in legendary_channels:
            self.channel_subscriptions[channel] = set()
    
    async def connect_user(self, websocket: WebSocket, user_id: str, username: str, 
                          is_legendary: bool = False) -> str:
        """Connect user to WebSocket with legendary handling"""
        
        await websocket.accept()
        
        connection_id = str(uuid.uuid4())
        connection = WebSocketConnection(
            websocket=websocket,
            user_id=user_id,
            username=username,
            connection_id=connection_id,
            connected_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc),
            is_legendary=is_legendary,
            status=UserStatus.LEGENDARY if is_legendary else UserStatus.ONLINE
        )
        
        # Store connection
        self.connections[connection_id] = connection
        self.user_connections[user_id].append(connection_id)
        
        # Auto-subscribe to default channels
        await self._auto_subscribe_user(connection)
        
        # Announce user connection
        await self._announce_user_status(user_id, username, UserStatus.LEGENDARY if is_legendary else UserStatus.ONLINE)
        
        # Special welcome for RICKROLL187
        if is_legendary and username == "rickroll187":
            await self._send_legendary_welcome(connection_id)
        
        # Store connection info in Redis for scaling
        connection_data = {
            "user_id": user_id,
            "username": username,
            "connected_at": connection.connected_at.isoformat(),
            "is_legendary": str(is_legendary),
            "status": connection.status.value
        }
        
        self.redis_client.hset(f"ws_connection:{connection_id}", mapping=connection_data)
        self.redis_client.expire(f"ws_connection:{connection_id}", 3600)  # 1 hour
        
        self.logger.info(f"🎸 {'Legendary founder' if is_legendary else 'User'} {username} connected: {connection_id}")
        
        return connection_id
    
    async def disconnect_user(self, connection_id: str):
        """Disconnect user with cleanup"""
        
        if connection_id not in self.connections:
            return
        
        connection = self.connections[connection_id]
        user_id = connection.user_id
        username = connection.username
        
        # Remove from subscriptions
        for channel in connection.subscribed_channels:
            self.channel_subscriptions[channel].discard(connection_id)
        
        # Remove connection
        del self.connections[connection_id]
        if connection_id in self.user_connections[user_id]:
            self.user_connections[user_id].remove(connection_id)
        
        # Clean up empty user connections
        if not self.user_connections[user_id]:
            del self.user_connections[user_id]
            # Announce user offline
            await self._announce_user_status(user_id, username, UserStatus.OFFLINE)
        
        # Clean up Redis data
        self.redis_client.delete(f"ws_connection:{connection_id}")
        
        self.logger.info(f"🎸 {'Legendary founder' if connection.is_legendary else 'User'} {username} disconnected: {connection_id}")
    
    async def _auto_subscribe_user(self, connection: WebSocketConnection):
        """Auto-subscribe user to relevant channels"""
        
        # Default channels for all users
        default_channels = ["general", "announcements", "system_alerts"]
        
        # Additional channels for legendary users
        if connection.is_legendary:
            default_channels.extend([
                "legendary_founder_channel",
                "swiss_precision_updates"
            ])
        
        for channel in default_channels:
            await self.subscribe_to_channel(connection.connection_id, channel)
    
    async def subscribe_to_channel(self, connection_id: str, channel: str) -> bool:
        """Subscribe connection to channel"""
        
        if connection_id not in self.connections:
            return False
        
        connection = self.connections[connection_id]
        connection.subscribed_channels.add(channel)
        self.channel_subscriptions[channel].add(connection_id)
        
        # Send subscription confirmation
        await self._send_to_connection(connection_id, {
            "type": "subscription_confirmed",
            "channel": channel,
            "message": f"🎸 Subscribed to {channel} with legendary precision! 🎸" if connection.is_legendary else f"Subscribed to {channel}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return True
    
    async def unsubscribe_from_channel(self, connection_id: str, channel: str) -> bool:
        """Unsubscribe connection from channel"""
        
        if connection_id not in self.connections:
            return False
        
        connection = self.connections[connection_id]
        connection.subscribed_channels.discard(channel)
        self.channel_subscriptions[channel].discard(connection_id)
        
        return True
    
    async def send_message(self, message: WebSocketMessage) -> int:
        """Send message with legendary delivery"""
        
        sent_count = 0
        
        # Determine recipients
        if message.recipients:
            # Send to specific users
            for user_id in message.recipients:
                sent_count += await self._send_to_user(user_id, message)
        
        elif message.channel:
            # Send to channel subscribers
            sent_count += await self._send_to_channel(message.channel, message)
        
        else:
            # Broadcast to all connections
            sent_count += await self._broadcast_message(message)
        
        # Store message in Redis for persistence
        await self._store_message(message)
        
        return sent_count
    
    async def _send_to_user(self, user_id: str, message: WebSocketMessage) -> int:
        """Send message to specific user"""
        
        sent_count = 0
        
        if user_id in self.user_connections:
            for connection_id in self.user_connections[user_id]:
                if await self._send_to_connection(connection_id, message.to_dict()):
                    sent_count += 1
        
        return sent_count
    
    async def _send_to_channel(self, channel: str, message: WebSocketMessage) -> int:
        """Send message to channel subscribers"""
        
        sent_count = 0
        
        if channel in self.channel_subscriptions:
            for connection_id in self.channel_subscriptions[channel].copy():
                if await self._send_to_connection(connection_id, message.to_dict()):
                    sent_count += 1
        
        return sent_count
    
    async def _broadcast_message(self, message: WebSocketMessage) -> int:
        """Broadcast message to all connections"""
        
        sent_count = 0
        
        for connection_id in list(self.connections.keys()):
            if await self._send_to_connection(connection_id, message.to_dict()):
                sent_count += 1
        
        return sent_count
    
    async def _send_to_connection(self, connection_id: str, data: Dict[str, Any]) -> bool:
        """Send data to specific connection"""
        
        if connection_id not in self.connections:
            return False
        
        connection = self.connections[connection_id]
        
        try:
            # Add legendary branding for legendary users
            if connection.is_legendary:
                data["legendary_status"] = True
                data["swiss_precision"] = True
            
            await connection.websocket.send_text(json.dumps(data))
            connection.last_activity = datetime.now(timezone.utc)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message to {connection_id}: {e}")
            # Disconnect broken connection
            await self.disconnect_user(connection_id)
            return False
    
    async def _announce_user_status(self, user_id: str, username: str, status: UserStatus):
        """Announce user status change"""
        
        status_message = WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.USER_STATUS,
            sender_id="system",
            sender_username="System",
            content={
                "user_id": user_id,
                "username": username,
                "status": status.value,
                "message": self._get_status_message(username, status),
                "is_legendary": status == UserStatus.LEGENDARY
            },
            channel="general"
        )
        
        await self.send_message(status_message)
    
    def _get_status_message(self, username: str, status: UserStatus) -> str:
        """Get status change message"""
        
        if status == UserStatus.LEGENDARY:
            return f"🎸 LEGENDARY FOUNDER {username} has joined! Swiss precision activated! 🎸"
        elif status == UserStatus.ONLINE:
            return f"👋 {username} is now online"
        elif status == UserStatus.OFFLINE:
            return f"👋 {username} went offline"
        elif status == UserStatus.AWAY:
            return f"😴 {username} is away"
        elif status == UserStatus.BUSY:
            return f"🔥 {username} is busy"
        
        return f"{username} status changed to {status.value}"
    
    async def _send_legendary_welcome(self, connection_id: str):
        """Send special welcome message for RICKROLL187"""
        
        welcome_data = {
            "type": "legendary_welcome",
            "title": "🎸 LEGENDARY FOUNDER CONNECTED! 🎸",
            "message": "Welcome back, RICKROLL187! Your legendary presence activates Swiss precision mode across the entire platform!",
            "features": [
                "🏆 All legendary features activated",
                "⚡ Swiss precision timing enabled", 
                "💪 Maximum code bro energy engaged",
                "🎯 Full system privileges granted",
                "😄 Joke cracking mode: MAXIMUM"
            ],
            "legendary_quote": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "legendary_status": True,
            "swiss_precision": True
        }
        
        await self._send_to_connection(connection_id, welcome_data)
    
    async def send_code_bro_joke(self, sender_id: str, sender_username: str, joke: str):
        """Send code bro joke to the team"""
        
        joke_message = WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.CODE_BRO_JOKE,
            sender_id=sender_id,
            sender_username=sender_username,
            content={
                "joke": joke,
                "emoji": "😂",
                "is_legendary_joke": sender_username == "rickroll187"
            },
            channel="code_bro_jokes",
            is_legendary=sender_username == "rickroll187"
        )
        
        await self.send_message(joke_message)
    
    async def send_performance_update(self, user_id: str, performance_data: Dict[str, Any]):
        """Send performance update notification"""
        
        update_message = WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.PERFORMANCE_UPDATE,
            sender_id="system",
            sender_username="Performance System",
            content=performance_data,
            recipients=[user_id]
        )
        
        await self.send_message(update_message)
    
    async def send_okr_update(self, user_id: str, okr_data: Dict[str, Any]):
        """Send OKR update notification"""
        
        update_message = WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.OKR_UPDATE,
            sender_id="system",
            sender_username="OKR System",
            content=okr_data,
            recipients=[user_id]
        )
        
        await self.send_message(update_message)
    
    async def send_system_alert(self, alert_data: Dict[str, Any], channel: str = "system_alerts"):
        """Send system alert"""
        
        alert_message = WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=MessageType.SYSTEM_ALERT,
            sender_id="system",
            sender_username="System Alert",
            content=alert_data,
            channel=channel
        )
        
        await self.send_message(alert_message)
    
    async def handle_message(self, connection_id: str, message_data: Dict[str, Any]):
        """Handle incoming WebSocket message"""
        
        if connection_id not in self.connections:
            return
        
        connection = self.connections[connection_id]
        connection.last_activity = datetime.now(timezone.utc)
        
        message_type = MessageType(message_data.get("type", "chat"))
        
        # Create message object
        message = WebSocketMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            sender_id=connection.user_id,
            sender_username=connection.username,
            content=message_data.get("content", ""),
            channel=message_data.get("channel"),
            recipients=message_data.get("recipients"),
            is_legendary=connection.is_legendary,
            metadata=message_data.get("metadata", {})
        )
        
        # Handle different message types
        if message_type == MessageType.CHAT:
            await self._handle_chat_message(message)
        elif message_type == MessageType.TYPING_INDICATOR:
            await self._handle_typing_indicator(message)
        elif message_type == MessageType.CODE_BRO_JOKE:
            await self._handle_code_bro_joke(message)
        else:
            # Default message handling
            await self.send_message(message)
    
    async def _handle_chat_message(self, message: WebSocketMessage):
        """Handle chat message with special processing"""
        
        # Add legendary formatting for RICKROLL187
        if message.is_legendary:
            if isinstance(message.content, str):
                message.content = f"🎸 {message.content} 🎸"
            elif isinstance(message.content, dict):
                message.content["legendary_message"] = True
        
        await self.send_message(message)
    
    async def _handle_typing_indicator(self, message: WebSocketMessage):
        """Handle typing indicator"""
        
        # Don't store typing indicators
        if message.channel:
            await self._send_to_channel(message.channel, message)
        elif message.recipients:
            for user_id in message.recipients:
                await self._send_to_user(user_id, message)
    
    async def _handle_code_bro_joke(self, message: WebSocketMessage):
        """Handle code bro joke with special processing"""
        
        if isinstance(message.content, str):
            await self.send_code_bro_joke(
                message.sender_id,
                message.sender_username,
                message.content
            )
    
    async def _store_message(self, message: WebSocketMessage):
        """Store message in Redis for persistence"""
        
        # Don't store typing indicators or temporary messages
        if message.message_type in [MessageType.TYPING_INDICATOR]:
            return
        
        message_key = f"ws_message:{message.message_id}"
        message_data = {
            "message_type": message.message_type.value,
            "sender_id": message.sender_id,
            "sender_username": message.sender_username,
            "content": json.dumps(message.content),
            "channel": message.channel or "",
            "recipients": json.dumps(message.recipients or []),
            "timestamp": message.timestamp.isoformat(),
            "is_legendary": str(message.is_legendary),
            "metadata": json.dumps(message.metadata)
        }
        
        self.redis_client.hset(message_key, mapping=message_data)
        self.redis_client.expire(message_key, 86400 * 7)  # Keep for 7 days
        
        # Add to channel history
        if message.channel:
            channel_key = f"ws_channel_history:{message.channel}"
            self.redis_client.lpush(channel_key, message.message_id)
            self.redis_client.ltrim(channel_key, 0, 999)  # Keep last 1000 messages
            self.redis_client.expire(channel_key, 86400 * 7)
    
    async def get_channel_history(self, channel: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get channel message history"""
        
        channel_key = f"ws_channel_history:{channel}"
        message_ids = self.redis_client.lrange(channel_key, 0, limit - 1)
        
        messages = []
        for message_id in message_ids:
            message_key = f"ws_message:{message_id.decode()}"
            message_data = self.redis_client.hgetall(message_key)
            
            if message_data:
                messages.append({
                    "message_id": message_id.decode(),
                    "message_type": message_data[b"message_type"].decode(),
                    "sender_id": message_data[b"sender_id"].decode(),
                    "sender_username": message_data[b"sender_username"].decode(),
                    "content": json.loads(message_data[b"content"].decode()),
                    "channel": message_data[b"channel"].decode(),
                    "timestamp": message_data[b"timestamp"].decode(),
                    "is_legendary": message_data[b"is_legendary"].decode() == "True"
                })
        
        return messages
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        
        total_connections = len(self.connections)
        legendary_connections = sum(1 for conn in self.connections.values() if conn.is_legendary)
        unique_users = len(self.user_connections)
        
        channel_stats = {}
        for channel, subscribers in self.channel_subscriptions.items():
            channel_stats[channel] = len(subscribers)
        
        return {
            "total_connections": total_connections,
            "legendary_connections": legendary_connections,
            "unique_users": unique_users,
            "channels": channel_stats,
            "legendary_message": "🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸" if legendary_connections > 0 else None
        }
    
    async def _heartbeat_task(self):
        """Background heartbeat task"""
        
        while True:
            try:
                await asyncio.sleep(30)  # Every 30 seconds
                
                # Send heartbeat to all connections
                heartbeat_data = {
                    "type": "heartbeat",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "server_status": "legendary_operational"
                }
                
                for connection_id in list(self.connections.keys()):
                    await self._send_to_connection(connection_id, heartbeat_data)
                
            except Exception as e:
                self.logger.error(f"Heartbeat task error: {e}")
    
    async def _cleanup_task(self):
        """Background cleanup task"""
        
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                # Clean up stale connections
                current_time = datetime.now(timezone.utc)
                stale_connections = []
                
                for connection_id, connection in self.connections.items():
                    # Mark as stale if no activity for 10 minutes
                    if (current_time - connection.last_activity).total_seconds() > 600:
                        stale_connections.append(connection_id)
                
                for connection_id in stale_connections:
                    await self.disconnect_user(connection_id)
                
                if stale_connections:
                    self.logger.info(f"Cleaned up {len(stale_connections)} stale connections")
                
            except Exception as e:
                self.logger.error(f"Cleanup task error: {e}")

# Add to WebSocketMessage class
def to_dict(message: WebSocketMessage) -> Dict[str, Any]:
    """Convert message to dictionary"""
    return {
        "message_id": message.message_id,
        "type": message.message_type.value,
        "sender_id": message.sender_id,
        "sender_username": message.sender_username,
        "content": message.content,
        "channel": message.channel,
        "recipients": message.recipients,
        "timestamp": message.timestamp.isoformat(),
        "is_legendary": message.is_legendary,
        "metadata": message.metadata
    }

# Monkey patch the method
WebSocketMessage.to_dict = to_dict

# Global WebSocket manager instance
legendary_ws_manager = LegendaryWebSocketManager()
