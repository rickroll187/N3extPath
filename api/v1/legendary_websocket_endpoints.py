# File: backend/api/v1/legendary_websocket_endpoints.py
"""
🌐🎸 N3EXTPATH - LEGENDARY WEBSOCKET ENDPOINTS 🎸🌐
Professional WebSocket API endpoints for real-time communication
Built: 2025-08-05 17:01:56 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import json
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from ..auth.legendary_auth_system import get_current_user, LegendaryUser
from ..websockets.legendary_websocket_manager import (
    legendary_ws_manager, 
    MessageType, 
    UserStatus,
    WebSocketMessage
)

# Create router for WebSocket endpoints
router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token"),
    channel: Optional[str] = Query(None, description="Initial channel to join")
):
    """
    🎸 Legendary WebSocket Connection Endpoint 🎸
    Connect to real-time communication with Swiss precision!
    """
    
    try:
        # Authenticate user from token
        from ..auth.legendary_auth_system import get_legendary_auth
        auth_system = get_legendary_auth()
        
        try:
            payload = auth_system.verify_token(token)
            user_id = payload["user_id"]
            username = payload["username"]
            is_legendary = payload.get("is_legendary", False)
        except Exception:
            await websocket.close(code=1008, reason="Authentication failed")
            return
        
        # Connect user to WebSocket
        connection_id = await legendary_ws_manager.connect_user(
            websocket, user_id, username, is_legendary
        )
        
        # Join initial channel if specified
        if channel:
            await legendary_ws_manager.subscribe_to_channel(connection_id, channel)
        
        # Send connection success message
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "connection_id": connection_id,
            "user_id": user_id,
            "username": username,
            "is_legendary": is_legendary,
            "message": f"🎸 {'Legendary founder' if is_legendary else 'User'} {username} connected successfully!",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "legendary_message": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!" if is_legendary else None
        }))
        
        # Handle incoming messages
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle the message
                await legendary_ws_manager.handle_message(connection_id, message_data)
                
        except WebSocketDisconnect:
            pass
        
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass
    
    finally:
        # Clean up connection
        if 'connection_id' in locals():
            await legendary_ws_manager.disconnect_user(connection_id)

@router.post("/send-message")
async def send_websocket_message(
    message_data: Dict[str, Any],
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Send WebSocket Message 🎸
    Send message through WebSocket system with legendary delivery!
    """
    
    # Create message
    message = WebSocketMessage(
        message_id=f"api_{datetime.now().timestamp()}",
        message_type=MessageType(message_data.get("type", "chat")),
        sender_id=current_user.user_id,
        sender_username=current_user.username,
        content=message_data.get("content"),
        channel=message_data.get("channel"),
        recipients=message_data.get("recipients"),
        is_legendary=current_user.is_legendary,
        metadata=message_data.get("metadata", {})
    )
    
    # Send message
    sent_count = await legendary_ws_manager.send_message(message)
    
    return {
        "success": True,
        "message_id": message.message_id,
        "sent_to": sent_count,
        "message": f"Message sent with {'legendary precision' if current_user.is_legendary else 'success'}!",
        "timestamp": message.timestamp.isoformat(),
        "legendary_delivery": current_user.is_legendary
    }

@router.post("/broadcast")
async def broadcast_message(
    broadcast_data: Dict[str, Any],
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Broadcast Message 🎸
    Broadcast message to all connected users (requires admin privileges)
    """
    
    # Check permissions (only admins and legendary users can broadcast)
    if not (current_user.role.value in ["admin", "legendary_founder"] or current_user.is_legendary):
        raise HTTPException(status_code=403, detail="Insufficient privileges for broadcasting")
    
    # Create broadcast message
    message = WebSocketMessage(
        message_id=f"broadcast_{datetime.now().timestamp()}",
        message_type=MessageType.LEGENDARY_ANNOUNCEMENT if current_user.is_legendary else MessageType.NOTIFICATION,
        sender_id=current_user.user_id,
        sender_username=current_user.username,
        content=broadcast_data.get("content"),
        is_legendary=current_user.is_legendary,
        metadata={
            "broadcast": True,
            "priority": broadcast_data.get("priority", "normal")
        }
    )
    
    # Broadcast to all connections
    sent_count = await legendary_ws_manager._broadcast_message(message)
    
    return {
        "success": True,
        "message_id": message.message_id,
        "broadcast_to": sent_count,
        "message": f"🎸 {'Legendary broadcast' if current_user.is_legendary else 'Broadcast'} sent to {sent_count} users!",
        "timestamp": message.timestamp.isoformat(),
        "legendary_broadcast": current_user.is_legendary
    }

@router.post("/send-joke")
async def send_code_bro_joke(
    joke_data: Dict[str, str],
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Send Code Bro Joke 🎸
    Share legendary jokes with the team!
    """
    
    joke = joke_data.get("joke", "")
    if not joke:
        raise HTTPException(status_code=400, detail="Joke content is required")
    
    # Send joke through WebSocket
    await legendary_ws_manager.send_code_bro_joke(
        current_user.user_id,
        current_user.username,
        joke
    )
    
    return {
        "success": True,
        "message": f"🎸 {'Legendary joke' if current_user.is_legendary else 'Code bro joke'} shared with the team!",
        "joke": joke,
        "legendary_joke": current_user.is_legendary,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/channels")
async def get_channels(
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Get Available Channels 🎸
    Get list of available WebSocket channels
    """
    
    # Base channels available to all users
    channels = [
        {
            "name": "general",
            "description": "General team communication",
            "type": "public",
            "legendary": False
        },
        {
            "name": "announcements",
            "description": "Company announcements",
            "type": "public",
            "legendary": False
        },
        {
            "name": "code_bro_jokes",
            "description": "Share jokes and have fun!",
            "type": "public",
            "legendary": False
        },
        {
            "name": "performance_updates",
            "description": "Performance review notifications",
            "type": "private",
            "legendary": False
        },
        {
            "name": "okr_updates",
            "description": "OKR progress notifications",
            "type": "private",
            "legendary": False
        }
    ]
    
    # Add legendary channels for RICKROLL187
    if current_user.is_legendary:
        channels.extend([
            {
                "name": "legendary_founder_channel",
                "description": "🎸 Exclusive legendary founder communications 🎸",
                "type": "legendary",
                "legendary": True
            },
            {
                "name": "swiss_precision_updates",
                "description": "⚡ Swiss precision system updates ⚡",
                "type": "legendary",
                "legendary": True
            }
        ])
    
    return {
        "success": True,
        "channels": channels,
        "total_channels": len(channels),
        "legendary_channels": len([c for c in channels if c["legendary"]]),
        "user_privileges": "legendary" if current_user.is_legendary else "standard"
    }

@router.get("/channel/{channel_name}/history")
async def get_channel_history(
    channel_name: str,
    limit: int = Query(50, ge=1, le=100, description="Number of messages to retrieve"),
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Get Channel History 🎸
    Retrieve message history for a channel
    """
    
    # Check access to legendary channels
    legendary_channels = ["legendary_founder_channel", "swiss_precision_updates"]
    if channel_name in legendary_channels and not current_user.is_legendary:
        raise HTTPException(status_code=403, detail="Access to legendary channels requires legendary status")
    
    # Get message history
    messages = await legendary_ws_manager.get_channel_history(channel_name, limit)
    
    return {
        "success": True,
        "channel": channel_name,
        "messages": messages,
        "total_messages": len(messages),
        "limit": limit,
        "legendary_access": current_user.is_legendary,
        "retrieved_at": datetime.now(timezone.utc).isoformat()
    }

@router.get("/stats")
async def get_websocket_stats(
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Get WebSocket Statistics 🎸
    Get real-time connection and usage statistics
    """
    
    # Check permissions for detailed stats
    if not (current_user.role.value in ["admin", "legendary_founder"] or current_user.is_legendary):
        raise HTTPException(status_code=403, detail="Insufficient privileges for detailed statistics")
    
    # Get connection stats
    stats = legendary_ws_manager.get_connection_stats()
    
    # Add additional stats for legendary users
    if current_user.is_legendary:
        stats.update({
            "legendary_founder_online": current_user.username in [
                conn.username for conn in legendary_ws_manager.connections.values() 
                if conn.is_legendary
            ],
            "swiss_precision_active": True,
            "code_bro_energy": "maximum",
            "system_status": "legendary_operational"
        })
    
    return {
        "success": True,
        "stats": stats,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "requested_by": current_user.username,
        "legendary_stats": current_user.is_legendary
    }

@router.post("/notify-performance-update")
async def notify_performance_update(
    notification_data: Dict[str, Any],
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Send Performance Update Notification 🎸
    Send performance update through WebSocket
    """
    
    target_user_id = notification_data.get("user_id")
    if not target_user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Check permissions (managers can notify their team members)
    if not (current_user.role.value in ["manager", "director", "admin", "legendary_founder"] or current_user.is_legendary):
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    
    # Send performance update notification
    await legendary_ws_manager.send_performance_update(target_user_id, notification_data)
    
    return {
        "success": True,
        "message": "Performance update notification sent",
        "target_user": target_user_id,
        "sent_by": current_user.username,
        "legendary_notification": current_user.is_legendary,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.post("/notify-okr-update")
async def notify_okr_update(
    notification_data: Dict[str, Any],
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Send OKR Update Notification 🎸
    Send OKR update through WebSocket
    """
    
    target_user_id = notification_data.get("user_id")
    if not target_user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    # Send OKR update notification
    await legendary_ws_manager.send_okr_update(target_user_id, notification_data)
    
    return {
        "success": True,
        "message": "OKR update notification sent",
        "target_user": target_user_id,
        "sent_by": current_user.username,
        "legendary_notification": current_user.is_legendary,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.post("/system-alert")
async def send_system_alert(
    alert_data: Dict[str, Any],
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎸 Send System Alert 🎸
    Send system alert to all users (admin only)
    """
    
    # Check admin permissions
    if not (current_user.role.value in ["admin", "legendary_founder"] or current_user.is_legendary):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    
    # Add sender information
    alert_data.update({
        "sent_by": current_user.username,
        "sender_role": current_user.role.value,
        "legendary_alert": current_user.is_legendary,
        "alert_id": f"alert_{datetime.now().timestamp()}"
    })
    
    # Send system alert
    await legendary_ws_manager.send_system_alert(alert_data)
    
    return {
        "success": True,
        "message": f"🎸 {'Legendary system alert' if current_user.is_legendary else 'System alert'} sent to all users",
        "alert_id": alert_data["alert_id"],
        "sent_by": current_user.username,
        "legendary_alert": current_user.is_legendary,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Add WebSocket router to main app
# This would be imported in your main FastAPI app file
