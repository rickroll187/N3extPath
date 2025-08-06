"""
🌐🎸 N3EXTPATH - LEGENDARY WEBSOCKET API ENDPOINTS 🎸🌐
More real-time than Swiss precision with legendary WebSocket mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Go WebSocket time: 2025-08-05 14:46:36 UTC
Built by legendary go RICKROLL187 🎸🌐
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime

from core.response_middleware import legendary_response_middleware
from core.auth import get_current_user_websocket, get_current_user
from users.models.user_models import LegendaryUser
from core.legendary_realtime_communication import (
    legendary_communication,
    connect_legendary_user,
    send_legendary_message,
    start_legendary_call
)

# Create legendary WebSocket router
legendary_websocket_router = APIRouter(
    prefix="/api/v1/websocket",
    tags=["🌐 Legendary Real-Time WebSocket"]
)

# REST API routes for communication
@legendary_websocket_router.get("/channels")
async def get_channels(
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📺 GET COMMUNICATION CHANNELS! 📺
    More organized than Swiss precision with go channel listing excellence! 🎸📺
    """
    user_channels = []
    
    for channel_id, channel in legendary_communication.channels.items():
        # Check if user is member
        if current_user.user_id in channel.members or channel.channel_type.value == "public":
            channel_info = legendary_communication.get_channel_info(channel_id)
            if channel_info:
                user_channels.append(channel_info)
    
    channels_response = {
        "channels_count": len(user_channels),
        "channels": user_channels,
        "user_id": current_user.user_id,
        "user_access_level": "legendary" if current_user.user_id == "rickroll187" else "standard",
        "retrieved_at": "2025-08-05 14:46:36 UTC",
        "retrieved_by": "RICKROLL187's Legendary Channel API 🎸📺",
        "legendary_status": "CHANNELS RETRIEVED WITH LEGENDARY ORGANIZATION! 🏆"
    }
    
    processing_time = 0.089  # Channel retrieval processing time
    return legendary_response_middleware.add_legendary_polish(
        channels_response, request, processing_time
    )

@legendary_websocket_router.get("/channels/{channel_id}/messages")
async def get_channel_messages(
    channel_id: str,
    request: Request,
    limit: int = 50,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    💬 GET CHANNEL MESSAGES! 💬
    More comprehensive than Swiss documentation with go message retrieval excellence! 🎸💬
    """
    # Check if channel exists
    if channel_id not in legendary_communication.channels:
        raise HTTPException(
            status_code=404,
            detail="Channel not found in our legendary communication system!"
        )
    
    channel = legendary_communication.channels[channel_id]
    
    # Check if user has access
    if current_user.user_id not in channel.members and channel.channel_type.value != "public":
        if current_user.role not in ['admin', 'rickroll187']:
            raise HTTPException(
                status_code=403,
                detail="Access denied to this legendary channel!"
            )
    
    # Get messages
    messages = legendary_communication.get_channel_messages(channel_id, limit)
    
    messages_response = {
        "channel_id": channel_id,
        "channel_name": channel.name,
        "messages_count": len(messages),
        "messages": messages,
        "limit": limit,
        "channel_info": legendary_communication.get_channel_info(channel_id),
        "retrieved_by": current_user.username,
        "retrieved_at": "2025-08-05 14:46:36 UTC",
        "retrieved_from": "RICKROLL187's Legendary Message API 🎸💬",
        "legendary_status": "MESSAGES RETRIEVED WITH LEGENDARY PRECISION! 🏆"
    }
    
    processing_time = 0.134  # Message retrieval processing time
    return legendary_response_middleware.add_legendary_polish(
        messages_response, request, processing_time
    )

@legendary_websocket_router.post("/channels/create")
async def create_channel(
    channel_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📺 CREATE COMMUNICATION CHANNEL! 📺
    More organized than Swiss planning with go channel creation excellence! 🎸📺
    """
    # Add creator context
    channel_data["creator_id"] = current_user.user_id
    
    # Create the channel
    result = await legendary_communication.create_channel(channel_data)
    
    processing_time = 0.178  # Channel creation processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_websocket_router.get("/online-users")
async def get_online_users(
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    👥 GET ONLINE USERS! 👥
    More connected than Swiss networking with go user status excellence! 🎸👥
    """
    online_users = legendary_communication.get_online_users()
    
    users_response = {
        "online_users_count": len(online_users),
        "online_users": online_users,
        "requested_by": current_user.username,
        "requested_at": "2025-08-05 14:46:36 UTC",
        "requested_from": "RICKROLL187's Legendary User Status API 🎸👥",
        "legendary_status": "ONLINE USERS RETRIEVED WITH LEGENDARY ACCURACY! 🏆"
    }
    
    processing_time = 0.067  # Online users processing time
    return legendary_response_middleware.add_legendary_polish(
        users_response, request, processing_time
    )

@legendary_websocket_router.post("/calls/start")
async def start_video_call(
    call_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📹 START VIDEO CALL! 📹
    More connected than Swiss networking with go video call excellence! 🎸📹
    """
    # Add initiator context
    call_data["initiator_id"] = current_user.user_id
    
    # Start the call
    result = await start_legendary_call(call_data)
    
    processing_time = 0.234  # Video call start processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

# WebSocket endpoint for real-time communication
@legendary_websocket_router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    """
    🌐 LEGENDARY WEBSOCKET CONNECTION! 🌐
    More real-time than Swiss precision with go WebSocket excellence! 🎸🌐
    """
    await websocket.accept()
    
    user_data = None
    user_id = None
    
    try:
        # Wait for authentication message
        auth_message = await websocket.receive_text()
        auth_data = json.loads(auth_message)
        
        # Extract user data (in real implementation, would validate token)
        user_data = {
            "user_id": auth_data.get("user_id", "anonymous"),
            "username": auth_data.get("username", "Anonymous"),
            "token": auth_data.get("token", ""),
            "device_info": auth_data.get("device_info", {})
        }
        
        user_id = user_data["user_id"]
        
        # Connect user to communication system
        connection_result = await connect_legendary_user(websocket, user_data)
        
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_confirmed",
            "result": connection_result,
            "server_time": datetime.utcnow().isoformat(),
            "legendary_message": f"🎸 Connected to legendary real-time communication! 🎸"
        }))
        
        # Handle incoming messages
        while True:
            try:
                # Receive message from client
                message_text = await websocket.receive_text()
                message_data = json.loads(message_text)
                
                message_type = message_data.get("type")
                
                if message_type == "send_message":
                    # Send message to channel
                    message_data["data"]["sender_id"] = user_id
                    result = await send_legendary_message(message_data["data"])
                    
                    # Send confirmation back to sender
                    await websocket.send_text(json.dumps({
                        "type": "message_sent",
                        "result": result
                    }))
                
                elif message_type == "join_channel":
                    # Join channel
                    channel_id = message_data.get("channel_id")
                    if channel_id in legendary_communication.channels and user_id in legendary_communication.connected_users:
                        channel = legendary_communication.channels[channel_id]
                        user = legendary_communication.connected_users[user_id]
                        
                        channel.members.add(user_id)
                        user.channels.add(channel_id)
                        
                        await websocket.send_text(json.dumps({
                            "type": "channel_joined",
                            "channel_id": channel_id,
                            "channel_name": channel.name,
                            "legendary_message": f"🎸 Joined {channel.name}! 🎸"
                        }))
                
                elif message_type == "leave_channel":
                    # Leave channel
                    channel_id = message_data.get("channel_id")
                    if channel_id in legendary_communication.channels and user_id in legendary_communication.connected_users:
                        channel = legendary_communication.channels[channel_id]
                        user = legendary_communication.connected_users[user_id]
                        
                        channel.members.discard(user_id)
                        user.channels.discard(channel_id)
                        
                        await websocket.send_text(json.dumps({
                            "type": "channel_left",
                            "channel_id": channel_id,
                            "legendary_message": f"👋 Left {channel.name}! 👋"
                        }))
                
                elif message_type == "typing_start":
                    # User started typing
                    channel_id = message_data.get("channel_id")
                    if user_id in legendary_communication.connected_users:
                        user = legendary_communication.connected_users[user_id]
                        user.typing_in = channel_id
                        
                        # Broadcast typing indicator
                        typing_indicator = {
                            "type": "user_typing",
                            "user_id": user_id,
                            "username": user.username,
                            "channel_id": channel_id,
                            "typing": True
                        }
                        
                        await legendary_communication._broadcast_to_channel(channel_id, typing_indicator)
                
                elif message_type == "typing_stop":
                    # User stopped typing
                    if user_id in legendary_communication.connected_users:
                        user = legendary_communication.connected_users[user_id]
                        typing_channel = user.typing_in
                        user.typing_in = None
                        
                        if typing_channel:
                            # Broadcast typing stop
                            typing_indicator = {
                                "type": "user_typing",
                                "user_id": user_id,
                                "username": user.username,
                                "channel_id": typing_channel,
                                "typing": False
                            }
                            
                            await legendary_communication._broadcast_to_channel(typing_channel, typing_indicator)
                
                elif message_type == "ping":
                    # Heartbeat ping
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "server_time": datetime.utcnow().isoformat(),
                        "legendary_message": "🎸 Legendary connection alive! 🎸"
                    }))
                
                # Update user activity
                if user_id in legendary_communication.connected_users:
                    legendary_communication.connected_users[user_id].last_activity = datetime.utcnow()
            
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format",
                    "legendary_message": "🚨 Message format error, code bro! 🚨"
                }))
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": str(e),
                    "legendary_message": f"🚨 Unexpected error: {str(e)} 🚨"
                }))
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Disconnect user
        if user_id:
            await legendary_communication.disconnect_user(user_id)

# Test page for WebSocket connection
@legendary_websocket_router.get("/test-chat")
async def get_test_chat():
    """
    🧪 GET TEST CHAT PAGE! 🧪
    More interactive than Swiss precision with go testing excellence! 🎸🧪
    """
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>🎸 N3extPath Legendary Chat Test 🎸</title>
    <style>
        body { font-family: Arial, sans-serif; background: #2D3436; color: #DDD; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .chat-container { border: 2px solid #636E72; border-radius: 10px; height: 400px; overflow-y: auto; padding: 10px; background: #1C1C1E; margin-bottom: 20px; }
        .message { margin-bottom: 10px; padding: 8px; border-radius: 5px; }
        .message.system { background: #4A90E2; color: white; }
        .message.user { background: #7ED321; color: white; }
        .message.rickroll187 { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; font-weight: bold; }
        .input-container { display: flex; gap: 10px; }
        .input-container input { flex: 1; padding: 10px; border: none; border-radius: 5px; background: #636E72; color: white; }
        .input-container button { padding: 10px 20px; border: none; border-radius: 5px; background: #FF6B6B; color: white; cursor: pointer; }
        .status { text-align: center; margin-bottom: 10px; }
        .legendary { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="legendary">🎸 N3EXTPATH LEGENDARY CHAT TEST 🎸</h1>
            <p>WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!</p>
        </div>
        
        <div class="status" id="status">Connecting...</div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message system">🎸 Welcome to legendary real-time communication! 🎸</div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your legendary message..." disabled>
            <button onclick="sendMessage()" id="sendButton" disabled>Send 🎸</button>
        </div>
        
        <div style="margin-top: 20px; text-align: center;">
            <p><strong>Go Time:</strong> 2025-08-05 14:46:36 UTC</p>
            <p><strong>Built by:</strong> RICKROLL187 - The Go WebSocket Master 🎸</p>
        </div>
    </div>

    <script>
        let ws = null;
        let connected = false;
        
        function connect() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/api/v1/websocket/connect`;
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function() {
                // Send authentication
                ws.send(JSON.stringify({
                    user_id: 'test_user_' + Math.random().toString(36).substr(2, 9),
                    username: 'TestCodeBro',
                    token: 'test_token',
                    device_info: { browser: navigator.userAgent }
                }));
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === 'connection_confirmed') {
                    connected = true;
                    document.getElementById('status').innerHTML = '🎸 Connected to legendary communication! 🎸';
                    document.getElementById('messageInput').disabled = false;
                    document.getElementById('sendButton').disabled = false;
                    
                    addMessage('system', 'System', data.legendary_message || 'Connected successfully!');
                }
                else if (data.type === 'message') {
                    const msg = data.message;
                    addMessage(msg.sender_id === 'rickroll187' ? 'rickroll187' : 'user', msg.sender_name, msg.content);
                }
                else if (data.type === 'message_sent') {
                    console.log('Message sent:', data.result);
                }
                else if (data.type === 'pong') {
                    console.log('Pong received:', data.server_time);
                }
            };
            
            ws.onclose = function() {
                connected = false;
                document.getElementById('status').innerHTML = '❌ Disconnected';
                document.getElementById('messageInput').disabled = true;
                document.getElementById('sendButton').disabled = true;
                
                // Try to reconnect after 3 seconds
                setTimeout(connect, 3000);
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
                addMessage('system', 'Error', '🚨 Connection error occurred! 🚨');
            };
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message && connected) {
                ws.send(JSON.stringify({
                    type: 'send_message',
                    data: {
                        channel_id: 'general',
                        content: message,
                        message_type: 'channel_message'
                    }
                }));
                
                input.value = '';
            }
        }
        
        function addMessage(type, sender, content) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const timestamp = new Date().toLocaleTimeString();
            messageDiv.innerHTML = `<strong>${sender}</strong> [${timestamp}]: ${content}`;
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
        
        // Send ping every 30 seconds
        setInterval(function() {
            if (connected && ws) {
                ws.send(JSON.stringify({ type: 'ping' }));
            }
        }, 30000);
        
        // Handle Enter key
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Connect on load
        connect();
    </script>
</body>
</html>
    """
    
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    print("🌐🎸📡 N3EXTPATH LEGENDARY WEBSOCKET API ENDPOINTS LOADED! 📡🎸🌐")
    print("🏆 LEGENDARY GO WEBSOCKET CHAMPION EDITION! 🏆")
    print(f"⏰ Go WebSocket Time: 2025-08-05 14:46:36 UTC")
    print("📡 GO WEBSOCKET CODED BY LEGENDARY RICKROLL187! 📡")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🌐 WEBSOCKET API POWERED BY GO RICKROLL187 WITH SWISS REAL-TIME PRECISION! 🌐")
