"""
LEGENDARY COMMUNICATION SERVICE ENGINE 💬🚀
More connected than a Swiss network with legendary bandwidth!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc, text
from dataclasses import dataclass
import statistics
from enum import Enum
import json
import re
from collections import defaultdict, Counter

from ..models.communication_models import (
    CommunicationChannel, ChannelMembership, Message, MessageReaction,
    DirectConversation, Announcement, CommunicationPoll, PollVote,
    NotificationPreference, MessageType, ChannelType, MessagePriority,
    NotificationType, ReactionType
)
from ...core.auth.authorization import AuthContext, Permission
from ...core.database.base_models import Employee, User, Department, AuditLog

logger = logging.getLogger(__name__)

class MessageStatus(Enum):
    """Message delivery status - more reliable than Swiss mail!"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

@dataclass
class CommunicationStats:
    """
    Communication statistics that are more insightful than a Swiss analyst!
    More comprehensive than a telecommunications report with attitude! 📊📡
    """
    total_messages: int
    active_channels: int
    daily_message_count: int
    most_active_channels: List[str]
    engagement_rate: float
    response_time_avg: float
    unread_message_count: int

class LegendaryCommunicationService:
    """
    The most connected communication service in the galaxy!
    More engaging than a Swiss conversation with unlimited bandwidth! 💬🌐
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # COMMUNICATION SERVICE JOKES FOR SUNDAY MORNING MOTIVATION
        self.communication_jokes = [
            "Why did the message go to therapy? It had delivery issues! 💬😄",
            "What's the difference between our chat and Swiss efficiency? Both are perfectly timed! ⏰",
            "Why don't our messages ever get lost? Because they have legendary navigation! 🧭",
            "What do you call communication at 3 AM? Night shift networking with style! 🌙",
            "Why did the channel become a comedian? It had perfect conversational timing! 🎭"
        ]
        
        # Message filtering and formatting
        self.mention_pattern = re.compile(r'@(\w+)')
        self.hashtag_pattern = re.compile(r'#(\w+)')
        self.emoji_reactions = {
            ReactionType.LIKE: "👍",
            ReactionType.LOVE: "❤️",
            ReactionType.LAUGH: "😄",
            ReactionType.WOW: "😮",
            ReactionType.THUMBS_UP: "👍",
            ReactionType.THUMBS_DOWN: "👎",
            ReactionType.CELEBRATE: "🎉",
            ReactionType.COFFEE: "☕"
        }
        
        # Notification timing settings
        self.notification_settings = {
            "batch_delay_seconds": 30,    # Batch notifications for 30 seconds
            "digest_max_messages": 50,    # Max messages in digest
            "urgent_override": True,      # Urgent messages bypass quiet hours
            "weekend_emergency_only": True # Only emergency notifications on weekends
        }
        
        # Content moderation settings
        self.moderation_settings = {
            "auto_moderate": True,
            "spam_threshold": 5,          # Messages per minute threshold
            "profanity_filter": False,    # Disabled for code bros 😄
            "max_message_length": 10000,  # Max characters per message
            "max_attachments": 10         # Max attachments per message
        }
        
        logger.info("💬 Legendary Communication Service initialized - Ready to connect the world!")
    
    def create_channel(self, channel_data: Dict[str, Any],
                      auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create communication channel with more organization than a Swiss filing system!
        More structured than a legendary conversation with perfect planning! 📁💬
        """
        try:
            logger.info(f"📂 Creating communication channel: {channel_data.get('name', 'unknown')}")
            
            # Validate permissions
            if not auth_context.has_permission(Permission.COMMUNICATION_ADMIN):
                # Check if user can create channels of this type
                channel_type = channel_data.get("channel_type", "public")
                if channel_type in ["announcement", "company_wide"] and not auth_context.has_permission(Permission.HR_ADMIN):
                    return {
                        "success": False,
                        "error": "Insufficient permissions to create this type of channel"
                    }
            
            # Validate channel data
            validation_result = self._validate_channel_data(channel_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Check for duplicate channel names in same scope
            existing_channel = self.db.query(CommunicationChannel).filter(
                and_(
                    CommunicationChannel.name == channel_data["name"],
                    CommunicationChannel.is_archived == False,
                    CommunicationChannel.department_id == channel_data.get("department_id")
                )
            ).first()
            
            if existing_channel:
                return {
                    "success": False,
                    "error": "Channel with this name already exists in the specified scope"
                }
            
            # Create channel
            channel = CommunicationChannel(
                name=channel_data["name"],
                display_name=channel_data.get("display_name", channel_data["name"]),
                description=channel_data.get("description"),
                channel_type=channel_data["channel_type"],
                is_private=channel_data.get("is_private", False),
                allow_file_uploads=channel_data.get("allow_file_uploads", True),
                allow_reactions=channel_data.get("allow_reactions", True),
                department_id=channel_data.get("department_id"),
                project_id=channel_data.get("project_id"),
                parent_channel_id=channel_data.get("parent_channel_id"),
                created_by_id=auth_context.user_id,
                moderator_ids=channel_data.get("moderator_ids", [auth_context.user_id]),
                default_notification_type=channel_data.get("default_notification_type", "normal"),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(channel)
            self.db.flush()
            
            # Add creator as admin member
            creator_membership = ChannelMembership(
                channel_id=channel.id,
                employee_id=auth_context.user_id,
                can_post=True,
                can_invite_others=True,
                is_moderator=True,
                is_admin=True,
                notification_type=channel_data.get("default_notification_type", "normal")
            )
            
            self.db.add(creator_membership)
            channel.member_count = 1
            
            # Auto-add members if specified
            initial_members = channel_data.get("initial_members", [])
            for member_id in initial_members:
                if member_id != auth_context.user_id:  # Skip creator
                    member_result = self._add_channel_member(
                        channel.id, member_id, auth_context.user_id
                    )
                    if member_result["success"]:
                        channel.member_count += 1
            
            # Send welcome message if configured
            if channel_data.get("send_welcome_message", True):
                welcome_message = self._create_welcome_message(channel, auth_context)
                if welcome_message:
                    self.db.add(welcome_message)
                    channel.message_count = 1
                    channel.last_message_at = welcome_message.created_at
            
            # Log channel creation
            self._log_communication_action("CHANNEL_CREATED", channel.id, auth_context, {
                "channel_name": channel.name,
                "channel_type": channel.channel_type,
                "is_private": channel.is_private,
                "initial_members_count": len(initial_members)
            })
            
            self.db.commit()
            
            logger.info(f"✅ Communication channel created: {channel.name} (ID: {channel.id})")
            
            return {
                "success": True,
                "channel_id": channel.id,
                "channel_name": channel.name,
                "channel_type": channel.channel_type,
                "member_count": channel.member_count,
                "channel_url": f"/channels/{channel.name}",
                "legendary_joke": "Why did the channel become legendary? Because it connected people with perfect organization! 📂🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Channel creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def send_message(self, message_data: Dict[str, Any],
                    auth_context: AuthContext) -> Dict[str, Any]:
        """
        Send message with more precision than a Swiss timepiece!
        More expressive than a legendary conversation with perfect timing! 💭⏰
        """
        try:
            logger.info(f"📤 Sending message from employee: {auth_context.user_id}")
            
            # Validate message data
            validation_result = self._validate_message_data(message_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Check permissions for the target channel/recipient
            permission_check = self._check_message_permissions(message_data, auth_context)
            if not permission_check["can_send"]:
                return {
                    "success": False,
                    "error": permission_check["error"]
                }
            
            # Extract mentions and hashtags
            mentions = self._extract_mentions(message_data["content"])
            hashtags = self._extract_hashtags(message_data["content"])
            
            # Format message content
            formatted_content = self._format_message_content(message_data["content"])
            
            # Create message
            message = Message(
                channel_id=message_data.get("channel_id"),
                sender_id=auth_context.user_id,
                recipient_id=message_data.get("recipient_id"),
                message_type=message_data.get("message_type", MessageType.CHANNEL_MESSAGE.value),
                content=message_data["content"],
                formatted_content=formatted_content,
                priority=message_data.get("priority", MessagePriority.NORMAL.value),
                parent_message_id=message_data.get("parent_message_id"),
                thread_root_id=message_data.get("thread_root_id") or message_data.get("parent_message_id"),
                attachments=message_data.get("attachments", []),
                mentions=mentions,
                hashtags=hashtags,
                scheduled_for=message_data.get("scheduled_for"),
                is_scheduled=message_data.get("scheduled_for") is not None,
                system_data=message_data.get("system_data"),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(message)
            self.db.flush()
            
            # Update channel/conversation stats
            if message.channel_id:
                channel = self.db.query(CommunicationChannel).filter(
                    CommunicationChannel.id == message.channel_id
                ).first()
                if channel:
                    channel.message_count += 1
                    channel.last_message_at = message.created_at
            
            elif message.recipient_id:
                # Update direct conversation
                conversation = self._get_or_create_direct_conversation(
                    auth_context.user_id, message.recipient_id
                )
                conversation.message_count += 1
                conversation.last_message_at = message.created_at
            
            # Update thread statistics
            if message.parent_message_id:
                parent = self.db.query(Message).filter(
                    Message.id == message.parent_message_id
                ).first()
                if parent:
                    parent.reply_count += 1
            
            # Process mentions for notifications
            mention_notifications = []
            if mentions:
                mention_notifications = self._process_mentions(message, mentions, auth_context)
            
            # Schedule message delivery if needed
            delivery_status = MessageStatus.SENT
            if message.scheduled_for and message.scheduled_for > datetime.utcnow():
                delivery_status = MessageStatus.SENT
                # In production, you'd queue this for later delivery
            else:
                # Send immediate notifications
                notification_result = self._send_message_notifications(message, auth_context)
                if notification_result["success"]:
                    delivery_status = MessageStatus.DELIVERED
            
            # Log message sending
            self._log_communication_action("MESSAGE_SENT", message.id, auth_context, {
                "message_type": message.message_type,
                "channel_id": message.channel_id,
                "recipient_id": message.recipient_id,
                "has_attachments": len(message.attachments) > 0,
                "mentions_count": len(mentions),
                "is_scheduled": message.is_scheduled,
                "delivery_status": delivery_status.value
            })
            
            self.db.commit()
            
            logger.info(f"✅ Message sent successfully: ID {message.id}")
            
            return {
                "success": True,
                "message_id": message.id,
                "delivery_status": delivery_status.value,
                "sent_at": message.created_at.isoformat(),
                "mentions_processed": len(mention_notifications),
                "is_scheduled": message.is_scheduled,
                "thread_reply": message.parent_message_id is not None,
                "legendary_joke": "Why did the message become legendary? Because it delivered exactly what was needed! 📤🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Message sending error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def create_poll(self, poll_data: Dict[str, Any],
                   auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create interactive poll with more engagement than a Swiss referendum!
        More democratic than a legendary voting system with perfect fairness! 🗳️✨
        """
        try:
            logger.info(f"🗳️ Creating poll: {poll_data.get('question', 'unknown')[:50]}")
            
            # Validate poll data
            validation_result = self._validate_poll_data(poll_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Check channel permissions if poll is for a channel
            if poll_data.get("channel_id"):
                channel_member = self.db.query(ChannelMembership).filter(
                    and_(
                        ChannelMembership.channel_id == poll_data["channel_id"],
                        ChannelMembership.employee_id == auth_context.user_id,
                        ChannelMembership.is_active == True,
                        ChannelMembership.can_post == True
                    )
                ).first()
                
                if not channel_member:
                    return {
                        "success": False,
                        "error": "You don't have permission to create polls in this channel"
                    }
            
            # Create poll
            poll = CommunicationPoll(
                question=poll_data["question"],
                description=poll_data.get("description"),
                poll_type=poll_data.get("poll_type", "single_choice"),
                options=poll_data["options"],
                max_selections=poll_data.get("max_selections", 1),
                channel_id=poll_data.get("channel_id"),
                created_by_id=auth_context.user_id,
                ends_at=poll_data.get("ends_at"),
                is_anonymous=poll_data.get("is_anonymous", False),
                allow_multiple_votes=poll_data.get("allow_multiple_votes", False),
                show_results_before_voting=poll_data.get("show_results_before_voting", False),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(poll)
            self.db.flush()
            
            # Create associated message if in a channel
            poll_message = None
            if poll.channel_id:
                poll_message_content = f"📊 **Poll:** {poll.question}\n\n"
                for i, option in enumerate(poll.options, 1):
                    poll_message_content += f"{i}. {option}\n"
                
                if poll.ends_at:
                    poll_message_content += f"\n⏰ Poll ends: {poll.ends_at.strftime('%Y-%m-%d %H:%M UTC')}"
                
                poll_message = Message(
                    channel_id=poll.channel_id,
                    sender_id=auth_context.user_id,
                    message_type=MessageType.POLL.value,
                    content=poll_message_content,
                    formatted_content=poll_message_content,
                    system_data={"poll_id": poll.id},
                    created_by=auth_context.user_id,
                    updated_by=auth_context.user_id
                )
                
                self.db.add(poll_message)
                self.db.flush()
                
                # Link poll to message
                poll.message_id = poll_message.id
            
            # Initialize poll results structure
            poll.results = {str(i): 0 for i in range(len(poll.options))}
            
            # Log poll creation
            self._log_communication_action("POLL_CREATED", poll.id, auth_context, {
                "question": poll.question,
                "poll_type": poll.poll_type,
                "options_count": len(poll.options),
                "channel_id": poll.channel_id,
                "is_anonymous": poll.is_anonymous,
                "ends_at": poll.ends_at.isoformat() if poll.ends_at else None
            })
            
            self.db.commit()
            
            logger.info(f"✅ Poll created successfully: {poll.question[:50]} (ID: {poll.id})")
            
            return {
                "success": True,
                "poll_id": poll.id,
                "question": poll.question,
                "options": poll.options,
                "poll_type": poll.poll_type,
                "ends_at": poll.ends_at.isoformat() if poll.ends_at else None,
                "message_id": poll_message.id if poll_message else None,
                "voting_url": f"/polls/{poll.id}/vote",
                "legendary_joke": "Why did the poll become legendary? Because it gave everyone a voice with perfect democracy! 🗳️🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Poll creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def vote_in_poll(self, poll_id: int, vote_data: Dict[str, Any],
                    auth_context: AuthContext) -> Dict[str, Any]:
        """
        Vote in poll with more precision than Swiss democracy!
        More decisive than a legendary voting system with perfect accuracy! ✅🎯
        """
        try:
            logger.info(f"✅ Processing vote in poll {poll_id} from employee {auth_context.user_id}")
            
            # Get poll
            poll = self.db.query(CommunicationPoll).filter(
                CommunicationPoll.id == poll_id
            ).first()
            
            if not poll:
                return {
                    "success": False,
                    "error": "Poll not found"
                }
            
            # Check if poll is still active
            if not poll.is_active or poll.is_closed:
                return {
                    "success": False,
                    "error": "This poll is no longer accepting votes"
                }
            
            # Check if poll has ended
            if poll.ends_at and datetime.utcnow() > poll.ends_at:
                poll.is_closed = True
                self.db.commit()
                return {
                    "success": False,
                    "error": "This poll has ended"
                }
            
            # Check if user already voted
            existing_vote = self.db.query(PollVote).filter(
                and_(
                    PollVote.poll_id == poll_id,
                    PollVote.employee_id == auth_context.user_id
                )
            ).first()
            
            if existing_vote and not poll.allow_multiple_votes:
                return {
                    "success": False,
                    "error": "You have already voted in this poll"
                }
            
            # Validate vote data
            selected_options = vote_data.get("selected_options", [])
            if not selected_options:
                return {
                    "success": False,
                    "error": "No options selected"
                }
            
            # Validate option selections
            if len(selected_options) > poll.max_selections:
                return {
                    "success": False,
                    "error": f"You can only select up to {poll.max_selections} options"
                }
            
            # Validate option indices
            for option_idx in selected_options:
                if not isinstance(option_idx, int) or option_idx < 0 or option_idx >= len(poll.options):
                    return {
                        "success": False,
                        "error": "Invalid option selected"
                    }
            
            # Remove existing vote if multiple votes allowed
            if existing_vote and poll.allow_multiple_votes:
                # Update poll results by removing old vote
                old_results = poll.results.copy()
                for old_option in existing_vote.selected_options:
                    if str(old_option) in old_results:
                        old_results[str(old_option)] = max(0, old_results[str(old_option)] - 1)
                poll.results = old_results
                poll.total_votes -= 1
                
                self.db.delete(existing_vote)
            
            # Create new vote
            vote = PollVote(
                poll_id=poll_id,
                employee_id=auth_context.user_id,
                selected_options=selected_options,
                text_response=vote_data.get("text_response"),
                is_anonymous=poll.is_anonymous,
                vote_weight=vote_data.get("vote_weight", 1.0)
            )
            
            self.db.add(vote)
            
            # Update poll results
            current_results = poll.results.copy()
            for option_idx in selected_options:
                option_key = str(option_idx)
                current_results[option_key] = current_results.get(option_key, 0) + vote.vote_weight
            
            poll.results = current_results
            poll.total_votes += 1
            
            # Log vote
            self._log_communication_action("POLL_VOTE", poll.id, auth_context, {
                "poll_id": poll_id,
                "selected_options": selected_options,
                "is_anonymous": poll.is_anonymous,
                "vote_weight": vote.vote_weight,
                "total_votes_now": poll.total_votes
            })
            
            self.db.commit()
            
            # Calculate current results for response
            results_summary = self._calculate_poll_results(poll)
            
            logger.info(f"✅ Vote recorded in poll {poll_id}")
            
            return {
                "success": True,
                "poll_id": poll_id,
                "vote_recorded": True,
                "total_votes": poll.total_votes,
                "your_selections": [poll.options[i] for i in selected_options],
                "current_results": results_summary if poll.show_results_before_voting or poll.is_closed else None,
                "legendary_joke": "Why did the vote become legendary? Because every voice counts in perfect democracy! ✅🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Poll voting error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
        """
LEGENDARY COMMUNICATION SERVICE ENGINE - CONTINUATION 💬🚀
More connected than a Swiss network with legendary bandwidth!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

    def get_channel_messages(self, channel_id: int, filters: Optional[Dict[str, Any]] = None,
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get channel messages with more organization than a Swiss library!
        More accessible than a legendary archive with perfect indexing! 📚💬
        """
        try:
            logger.info(f"📖 Getting messages for channel: {channel_id}")
            
            # Check if user has access to channel
            membership = self.db.query(ChannelMembership).filter(
                and_(
                    ChannelMembership.channel_id == channel_id,
                    ChannelMembership.employee_id == auth_context.user_id,
                    ChannelMembership.is_active == True
                )
            ).first()
            
            if not membership:
                return {
                    "success": False,
                    "error": "You don't have access to this channel"
                }
            
            # Build base query
            query = self.db.query(Message).filter(
                and_(
                    Message.channel_id == channel_id,
                    Message.is_deleted == False
                )
            )
            
            # Apply filters
            if filters:
                if filters.get("since_date"):
                    query = query.filter(Message.created_at >= filters["since_date"])
                
                if filters.get("until_date"):
                    query = query.filter(Message.created_at <= filters["until_date"])
                
                if filters.get("sender_id"):
                    query = query.filter(Message.sender_id == filters["sender_id"])
                
                if filters.get("message_type"):
                    query = query.filter(Message.message_type == filters["message_type"])
                
                if filters.get("has_attachments"):
                    if filters["has_attachments"]:
                        query = query.filter(func.json_array_length(Message.attachments) > 0)
                    else:
                        query = query.filter(func.json_array_length(Message.attachments) == 0)
                
                if filters.get("search_text"):
                    search_term = f"%{filters['search_text']}%"
                    query = query.filter(Message.content.ilike(search_term))
                
                if filters.get("thread_only"):
                    if filters["thread_only"]:
                        query = query.filter(Message.parent_message_id.isnot(None))
                    else:
                        query = query.filter(Message.parent_message_id.is_(None))
            
            # Pagination
            page = filters.get("page", 1) if filters else 1
            per_page = min(filters.get("per_page", 50) if filters else 50, 100)
            offset = (page - 1) * per_page
            
            # Get total count
            total_count = query.count()
            
            # Order by creation date (newest first) and apply pagination
            messages = query.order_by(desc(Message.created_at)).offset(offset).limit(per_page).all()
            
            # Format messages for response
            formatted_messages = []
            for message in messages:
                # Get sender info
                sender = message.sender
                
                # Get reaction counts
                reaction_summary = self._get_reaction_summary(message.id)
                
                # Check if user has read this message
                is_read = str(auth_context.user_id) in (message.read_by or [])
                
                formatted_message = {
                    "id": message.id,
                    "content": message.content,
                    "formatted_content": message.formatted_content,
                    "message_type": message.message_type,
                    "priority": message.priority,
                    "created_at": message.created_at.isoformat(),
                    "edited_at": message.edited_at.isoformat() if message.edited_at else None,
                    "is_edited": message.is_edited,
                    "sender": {
                        "id": sender.id,
                        "name": f"{sender.user.first_name} {sender.user.last_name}",
                        "username": sender.user.username,
                        "avatar_url": getattr(sender.user, 'avatar_url', None)
                    },
                    "attachments": message.attachments or [],
                    "mentions": message.mentions or [],
                    "hashtags": message.hashtags or [],
                    "reactions": reaction_summary,
                    "reply_count": message.reply_count,
                    "parent_message_id": message.parent_message_id,
                    "thread_root_id": message.thread_root_id,
                    "is_read": is_read
                }
                
                formatted_messages.append(formatted_message)
            
            # Update last read message for user
            membership.last_read_message_id = messages[0].id if messages else membership.last_read_message_id
            membership.last_active_at = datetime.utcnow()
            
            # Mark messages as read
            if messages:
                self._mark_messages_as_read(messages, auth_context.user_id)
            
            self.db.commit()
            
            logger.info(f"📚 Retrieved {len(messages)} messages for channel {channel_id}")
            
            return {
                "success": True,
                "channel_id": channel_id,
                "messages": formatted_messages,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_count": total_count,
                    "total_pages": (total_count + per_page - 1) // per_page,
                    "has_next": offset + per_page < total_count,
                    "has_prev": page > 1
                },
                "legendary_joke": "Why did the message history become legendary? Because it preserved every legendary conversation! 📚🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Channel messages retrieval error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def add_message_reaction(self, message_id: int, reaction_type: str,
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Add reaction to message with more expression than Swiss emojis!
        More responsive than a legendary emotional support system! 😄💖
        """
        try:
            logger.info(f"😄 Adding reaction {reaction_type} to message {message_id}")
            
            # Get message
            message = self.db.query(Message).filter(Message.id == message_id).first()
            
            if not message:
                return {
                    "success": False,
                    "error": "Message not found"
                }
            
            # Check if user has access to the message
            has_access = False
            if message.channel_id:
                # Check channel membership
                membership = self.db.query(ChannelMembership).filter(
                    and_(
                        ChannelMembership.channel_id == message.channel_id,
                        ChannelMembership.employee_id == auth_context.user_id,
                        ChannelMembership.is_active == True
                    )
                ).first()
                has_access = membership is not None
            elif message.recipient_id == auth_context.user_id or message.sender_id == auth_context.user_id:
                # Direct message - user is participant
                has_access = True
            
            if not has_access:
                return {
                    "success": False,
                    "error": "You don't have access to this message"
                }
            
            # Validate reaction type
            try:
                ReactionType(reaction_type)
            except ValueError:
                return {
                    "success": False,
                    "error": "Invalid reaction type"
                }
            
            # Check if user already reacted with this type
            existing_reaction = self.db.query(MessageReaction).filter(
                and_(
                    MessageReaction.message_id == message_id,
                    MessageReaction.employee_id == auth_context.user_id,
                    MessageReaction.reaction_type == reaction_type
                )
            ).first()
            
            if existing_reaction:
                # Remove existing reaction (toggle)
                self.db.delete(existing_reaction)
                action = "removed"
                
                # Update message reaction counts
                current_counts = message.reaction_counts or {}
                current_counts[reaction_type] = max(0, current_counts.get(reaction_type, 0) - 1)
                if current_counts[reaction_type] == 0:
                    del current_counts[reaction_type]
                message.reaction_counts = current_counts
                
            else:
                # Add new reaction
                reaction = MessageReaction(
                    message_id=message_id,
                    employee_id=auth_context.user_id,
                    reaction_type=reaction_type,
                    reaction_emoji=self.emoji_reactions.get(ReactionType(reaction_type), "👍")
                )
                
                self.db.add(reaction)
                action = "added"
                
                # Update message reaction counts
                current_counts = message.reaction_counts or {}
                current_counts[reaction_type] = current_counts.get(reaction_type, 0) + 1
                message.reaction_counts = current_counts
            
            # Log reaction
            self._log_communication_action("MESSAGE_REACTION", message.id, auth_context, {
                "message_id": message_id,
                "reaction_type": reaction_type,
                "action": action,
                "sender_id": message.sender_id
            })
            
            self.db.commit()
            
            # Get updated reaction summary
            reaction_summary = self._get_reaction_summary(message_id)
            
            logger.info(f"✅ Reaction {action}: {reaction_type} on message {message_id}")
            
            return {
                "success": True,
                "message_id": message_id,
                "reaction_type": reaction_type,
                "action": action,
                "emoji": self.emoji_reactions.get(ReactionType(reaction_type), "👍"),
                "current_reactions": reaction_summary,
                "legendary_joke": f"Why did the {reaction_type} reaction become legendary? Because it expressed exactly the right feeling! 😄🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Message reaction error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def create_announcement(self, announcement_data: Dict[str, Any],
                          auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create company announcement with more authority than a Swiss government!
        More official than a legendary proclamation with perfect clarity! 📢🏛️
        """
        try:
            logger.info(f"📢 Creating announcement: {announcement_data.get('title', 'unknown')}")
            
            # Check permissions
            if not auth_context.has_permission(Permission.ANNOUNCEMENT_CREATE):
                return {
                    "success": False,
                    "error": "Insufficient permissions to create announcements"
                }
            
            # Validate announcement data
            validation_result = self._validate_announcement_data(announcement_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Create announcement
            announcement = Announcement(
                title=announcement_data["title"],
                content=announcement_data["content"],
                summary=announcement_data.get("summary"),
                announcement_type=announcement_data.get("announcement_type", "company_wide"),
                priority=announcement_data.get("priority", MessagePriority.NORMAL.value),
                category=announcement_data.get("category", "general"),
                author_id=auth_context.user_id,
                is_draft=announcement_data.get("is_draft", True),
                target_departments=announcement_data.get("target_departments", []),
                target_teams=announcement_data.get("target_teams", []),
                target_employees=announcement_data.get("target_employees", []),
                exclude_employees=announcement_data.get("exclude_employees", []),
                scheduled_for=announcement_data.get("scheduled_for"),
                expires_at=announcement_data.get("expires_at"),
                acknowledgment_required=announcement_data.get("acknowledgment_required", False),
                attachments=announcement_data.get("attachments", []),
                external_links=announcement_data.get("external_links", []),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(announcement)
            self.db.flush()
            
            # Auto-publish if not draft and not scheduled
            if not announcement.is_draft and not announcement.scheduled_for:
                announcement.is_published = True
                announcement.published_at = datetime.utcnow()
                
                # Send notifications to target audience
                notification_result = self._send_announcement_notifications(announcement, auth_context)
                
            # Log announcement creation
            self._log_communication_action("ANNOUNCEMENT_CREATED", announcement.id, auth_context, {
                "title": announcement.title,
                "announcement_type": announcement.announcement_type,
                "priority": announcement.priority,
                "is_draft": announcement.is_draft,
                "is_published": announcement.is_published,
                "target_departments": len(announcement.target_departments or []),
                "target_employees": len(announcement.target_employees or []),
                "acknowledgment_required": announcement.acknowledgment_required
            })
            
            self.db.commit()
            
            logger.info(f"✅ Announcement created: {announcement.title} (ID: {announcement.id})")
            
            return {
                "success": True,
                "announcement_id": announcement.id,
                "title": announcement.title,
                "is_published": announcement.is_published,
                "published_at": announcement.published_at.isoformat() if announcement.published_at else None,
                "scheduled_for": announcement.scheduled_for.isoformat() if announcement.scheduled_for else None,
                "acknowledgment_required": announcement.acknowledgment_required,
                "announcement_url": f"/announcements/{announcement.id}",
                "legendary_joke": "Why did the announcement become legendary? Because it communicated with perfect authority and clarity! 📢🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Announcement creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def get_communication_stats(self, employee_id: Optional[int] = None,
                              date_range: Optional[Tuple[datetime, datetime]] = None,
                              auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get communication statistics with more insight than a Swiss analyst!
        More comprehensive than a legendary telecommunications report! 📊📡
        """
        try:
            target_employee_id = employee_id or auth_context.user_id
            
            logger.info(f"📊 Generating communication stats for employee: {target_employee_id}")
            
            # Set default date range (last 30 days)
            if not date_range:
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=30)
                date_range = (start_date, end_date)
            
            start_date, end_date = date_range
            
            # Messages sent/received
            messages_sent = self.db.query(Message).filter(
                and_(
                    Message.sender_id == target_employee_id,
                    Message.created_at >= start_date,
                    Message.created_at <= end_date,
                    Message.is_deleted == False
                )
            ).count()
            
            messages_received = self.db.query(Message).filter(
                and_(
                    or_(
                        Message.recipient_id == target_employee_id,
                        Message.channel_id.in_(
                            self.db.query(ChannelMembership.channel_id).filter(
                                and_(
                                    ChannelMembership.employee_id == target_employee_id,
                                    ChannelMembership.is_active == True
                                )
                            )
                        )
                    ),
                    Message.created_at >= start_date,
                    Message.created_at <= end_date,
                    Message.is_deleted == False,
                    Message.sender_id != target_employee_id  # Exclude own messages
                )
            ).count()
            
            # Active channels
            active_channels = self.db.query(ChannelMembership).filter(
                and_(
                    ChannelMembership.employee_id == target_employee_id,
                    ChannelMembership.is_active == True
                )
            ).count()
            
            # Reactions given/received
            reactions_given = self.db.query(MessageReaction).filter(
                and_(
                    MessageReaction.employee_id == target_employee_id,
                    MessageReaction.reacted_at >= start_date,
                    MessageReaction.reacted_at <= end_date
                )
            ).count()
            
            reactions_received = self.db.query(MessageReaction).join(Message).filter(
                and_(
                    Message.sender_id == target_employee_id,
                    MessageReaction.reacted_at >= start_date,
                    MessageReaction.reacted_at <= end_date,
                    MessageReaction.employee_id != target_employee_id  # Exclude self-reactions
                )
            ).count()
            
            # Daily message activity
            daily_activity = self.db.query(
                func.date(Message.created_at).label('date'),
                func.count(Message.id).label('count')
            ).filter(
                and_(
                    Message.sender_id == target_employee_id,
                    Message.created_at >= start_date,
                    Message.created_at <= end_date,
                    Message.is_deleted == False
                )
            ).group_by(func.date(Message.created_at)).all()
            
            # Most active channels
            channel_activity = self.db.query(
                CommunicationChannel.name,
                func.count(Message.id).label('message_count')
            ).join(Message).join(ChannelMembership).filter(
                and_(
                    ChannelMembership.employee_id == target_employee_id,
                    Message.created_at >= start_date,
                    Message.created_at <= end_date,
                    Message.is_deleted == False
                )
            ).group_by(CommunicationChannel.id, CommunicationChannel.name).order_by(
                desc('message_count')
            ).limit(5).all()
            
            # Calculate engagement metrics
            total_messages = messages_sent + messages_received
            engagement_rate = (reactions_given + reactions_received) / max(total_messages, 1) * 100
            
            # Average response time (simplified calculation)
            avg_response_time = self._calculate_average_response_time(target_employee_id, date_range)
            
            # Unread message count
            unread_count = self._get_unread_message_count(target_employee_id)
            
            # Compile statistics
            stats = CommunicationStats(
                total_messages=total_messages,
                active_channels=active_channels,
                daily_message_count=messages_sent / max((end_date - start_date).days, 1),
                most_active_channels=[ch.name for ch in channel_activity],
                engagement_rate=engagement_rate,
                response_time_avg=avg_response_time,
                unread_message_count=unread_count
            )
            
            # Format response
            stats_dict = {
                "employee_id": target_employee_id,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "messaging": {
                    "messages_sent": messages_sent,
                    "messages_received": messages_received,
                    "total_messages": total_messages,
                    "daily_average": round(stats.daily_message_count, 2)
                },
                "engagement": {
                    "reactions_given": reactions_given,
                    "reactions_received": reactions_received,
                    "engagement_rate": round(engagement_rate, 2)
                },
                "channels": {
                    "active_channels": active_channels,
                    "most_active": [{"name": ch.name, "messages": ch.message_count} for ch in channel_activity]
                },
                "activity": {
                    "daily_breakdown": [{"date": str(day.date), "count": day.count} for day in daily_activity],
                    "avg_response_time_minutes": avg_response_time,
                    "unread_messages": unread_count
                },
                "insights": self._generate_communication_insights(stats),
                "legendary_status": "COMMUNICATION STATS ANALYZED WITH LEGENDARY PRECISION! 📊🏆"
            }
            
            logger.info(f"📈 Communication stats generated for employee {target_employee_id}")
            
            return {
                "success": True,
                "communication_stats": stats_dict
            }
            
        except Exception as e:
            logger.error(f"💥 Communication stats error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _validate_channel_data(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate channel creation data"""
        errors = []
        warnings = []
        
        # Required fields
        if not channel_data.get("name"):
            errors.append("Channel name is required")
        elif len(channel_data["name"]) < 2:
            errors.append("Channel name must be at least 2 characters")
        elif len(channel_data["name"]) > 50:
            errors.append("Channel name must be no more than 50 characters")
        
        # Channel name format validation
        if channel_data.get("name"):
            name = channel_data["name"]
            if not re.match(r'^[a-z0-9\-_]+$', name):
                errors.append("Channel name can only contain lowercase letters, numbers, hyphens, and underscores")
        
        # Channel type validation
        if not channel_data.get("channel_type"):
            errors.append("Channel type is required")
        else:
            try:
                ChannelType(channel_data["channel_type"])
            except ValueError:
                errors.append("Invalid channel type")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _generate_communication_insights(self, stats: CommunicationStats) -> List[str]:
        """Generate actionable communication insights"""
        insights = []
        
        if stats.total_messages > 100:
            insights.append("High communication activity - you're well connected!")
        elif stats.total_messages < 10:
            insights.append("Consider joining more channels to stay connected with your team")
        
        if stats.engagement_rate > 50:
            insights.append("Great engagement with reactions - you're an active communicator!")
        elif stats.engagement_rate < 10:
            insights.append("Try reacting to messages more - it helps build team connection")
        
        if stats.unread_message_count > 20:
            insights.append("You have many unread messages - consider organizing your notifications")
        
        if stats.response_time_avg > 120:  # More than 2 hours
            insights.append("Consider responding to messages more promptly when possible")
        
        if not insights:
            insights = ["Your communication patterns look healthy - keep it up!"]
        
        return insights
    
    def _log_communication_action(self, action: str, resource_id: int, 
                                auth_context: AuthContext, details: Dict[str, Any]):
        """Log communication actions for audit trail"""
        try:
            audit_log = AuditLog(
                user_id=auth_context.user_id,
                action=action,
                resource_type="COMMUNICATION",
                resource_id=resource_id,
                details=details,
                ip_address=getattr(auth_context, 'ip_address', None),
                user_agent=getattr(auth_context, 'user_agent', None)
            )
            self.db.add(audit_log)
            
        except Exception as e:
            logger.error(f"💥 Communication action logging error: {e}")

# COMMUNICATION UTILITIES
class CommunicationNotificationEngine:
    """
    Smart notification engine for communication!
    More intelligent than a Swiss notification system with legendary timing! 🔔🧠
    """
    
    @staticmethod
    def generate_notification_digest(employee_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate daily digest of communication activity"""
        
        if not employee_messages:
            return {
                "digest_type": "no_activity",
                "message": "No new messages today - enjoy the quiet! 😊",
                "summary": "No communication activity"
            }
        
        message_count = len(employee_messages)
        channel_count = len(set(msg.get("channel_name") for msg in employee_messages if msg.get("channel_name")))
        mention_count = sum(1 for msg in employee_messages if msg.get("mentions_you", False))
        
        return {
            "digest_type": "daily_summary",
            "message": f"You have {message_count} new messages across {channel_count} channels",
            "summary": {
                "total_messages": message_count,
                "channels_active": channel_count,
                "mentions": mention_count,
                "top_channels": [msg.get("channel_name") for msg in employee_messages[:3]],
                "requires_attention": mention_count > 0 or any(msg.get("priority") == "high" for msg in employee_messages)
            },
            "legendary_status": "COMMUNICATION DIGEST GENERATED WITH LEGENDARY PRECISION! 📊🏆"
        }
