# File: backend/ai/legendary_chat_assistant.py
"""
💬🎸 N3EXTPATH - LEGENDARY AI CHAT ASSISTANT 🎸💬
Professional AI-powered chat assistant for HR support and guidance
Built: 2025-08-05 16:18:21 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    """Chat message types"""
    QUESTION = "question"
    RESPONSE = "response"
    SYSTEM = "system"
    LEGENDARY = "legendary"

class IntentType(Enum):
    """User intent categories"""
    PERFORMANCE_QUERY = "performance_query"
    OKR_HELP = "okr_help"
    POLICY_QUESTION = "policy_question"
    CAREER_GUIDANCE = "career_guidance"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_HR = "general_hr"
    LEGENDARY_INTERACTION = "legendary_interaction"
    SMALL_TALK = "small_talk"

@dataclass
class ChatMessage:
    """Chat message data structure"""
    message_id: str
    user_id: str
    message_type: MessageType
    content: str
    intent: Optional[IntentType] = None
    confidence: float = 0.0
    timestamp: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}

class LegendaryChatAssistant:
    """Professional AI-Powered HR Chat Assistant"""
    
    def __init__(self):
        self.conversation_history = {}
        self.knowledge_base = self._initialize_knowledge_base()
        self.intent_patterns = self._initialize_intent_patterns()
        self.response_templates = self._initialize_response_templates()
        
        # Special legendary responses for RICKROLL187
        self.legendary_responses = self._initialize_legendary_responses()
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize HR knowledge base"""
        return {
            "policies": {
                "vacation": {
                    "annual_days": 25,
                    "carryover_limit": 5,
                    "approval_process": "Submit request through N3EXTPATH platform, manager approval required",
                    "blackout_dates": ["December 20-31", "First week of fiscal year"]
                },
                "remote_work": {
                    "policy": "Hybrid work model - up to 3 days remote per week",
                    "equipment": "Company provides laptop, monitor, and $500 home office stipend",
                    "requirements": "Maintain team collaboration and meeting attendance"
                },
                "professional_development": {
                    "budget": "$2000 per year per employee",
                    "approval": "Manager approval required for courses over $500",
                    "conference_policy": "One major conference per year covered"
                }
            },
            "processes": {
                "performance_review": {
                    "frequency": "Quarterly reviews with annual comprehensive review",
                    "process": "Self-assessment, peer feedback, manager evaluation, goal setting",
                    "timeline": "Reviews due first week of each quarter"
                },
                "okr_process": {
                    "timeline": "Set quarterly, reviewed monthly, updated bi-weekly",
                    "structure": "3-5 objectives, 3-4 key results each",
                    "scoring": "0.0-1.0 scale, 0.7 is target achievement"
                }
            },
            "benefits": {
                "health_insurance": "Full premium coverage for employee, 80% for family",
                "retirement": "6% match on 401k contributions",
                "wellness": "$100/month wellness stipend",
                "parental_leave": "12 weeks paid leave for primary caregiver"
            },
            "career_paths": {
                "engineering": ["Junior → Mid → Senior → Staff → Principal → Distinguished"],
                "management": ["Individual Contributor → Team Lead → Manager → Director → VP"],
                "legendary": ["🎸 RICKROLL187 - Legendary Founder Path 🎸"]
            }
        }
    
    def _initialize_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Initialize intent recognition patterns"""
        return {
            IntentType.PERFORMANCE_QUERY: [
                r"performance review", r"review process", r"feedback", r"rating", r"evaluation",
                r"how am i doing", r"performance score", r"improvement"
            ],
            IntentType.OKR_HELP: [
                r"okr", r"objectives", r"key results", r"goals", r"quarterly",
                r"target", r"progress", r"scoring", r"okr process"
            ],
            IntentType.POLICY_QUESTION: [
                r"policy", r"vacation", r"time off", r"remote work", r"pto",
                r"holiday", r"sick leave", r"benefits", r"insurance"
            ],
            IntentType.CAREER_GUIDANCE: [
                r"career", r"promotion", r"advancement", r"growth", r"next level",
                r"skill development", r"training", r"mentorship", r"leadership"
            ],
            IntentType.TECHNICAL_SUPPORT: [
                r"technical issue", r"bug", r"error", r"not working", r"login problem",
                r"password", r"access", r"support", r"help with system"
            ],
            IntentType.GENERAL_HR: [
                r"hr", r"human resources", r"employee", r"workplace", r"team",
                r"manager", r"colleague", r"work environment"
            ],
            IntentType.LEGENDARY_INTERACTION: [
                r"rickroll187", r"legendary", r"founder", r"code bros", r"swiss precision",
                r"legendary founder", r"code bro", r"jokes"
            ],
            IntentType.SMALL_TALK: [
                r"hello", r"hi", r"how are you", r"good morning", r"good afternoon",
                r"thanks", r"thank you", r"bye", r"goodbye"
            ]
        }
    
    def _initialize_response_templates(self) -> Dict[IntentType, List[str]]:
        """Initialize response templates for each intent"""
        return {
            IntentType.PERFORMANCE_QUERY: [
                "I can help you with performance-related questions! Our performance review process includes quarterly reviews with peer feedback and goal setting. Would you like me to explain any specific aspect?",
                "Performance reviews at N3EXTPATH are comprehensive and constructive. We focus on growth and development. What specific performance topic can I help you with?",
                "Great question about performance! We use a collaborative approach with self-assessments, peer feedback, and manager evaluations. Need details on any particular part?"
            ],
            IntentType.OKR_HELP: [
                "OKRs (Objectives and Key Results) are our goal-setting framework! We set them quarterly with 3-5 objectives and 3-4 key results each. Scoring is on a 0.0-1.0 scale where 0.7 is considered target achievement. What would you like to know?",
                "I'd be happy to help with OKRs! Our process involves quarterly goal setting with monthly reviews and bi-weekly updates. Would you like guidance on writing effective OKRs or tracking progress?",
                "OKRs drive our success at N3EXTPATH! They should be ambitious but achievable. Need help crafting your objectives or measuring key results?"
            ],
            IntentType.POLICY_QUESTION: [
                "I can help clarify our policies! We have comprehensive guidelines for vacation (25 days annually), remote work (up to 3 days/week), and professional development ($2000 annual budget). What specific policy interests you?",
                "Policy questions are important! Our employee handbook covers everything from benefits to work arrangements. Which policy area would you like me to explain?",
                "Happy to help with policy information! We believe in clear, fair policies that support work-life balance and professional growth. What can I clarify for you?"
            ],
            IntentType.CAREER_GUIDANCE: [
                "Career development is crucial at N3EXTPATH! We have clear advancement paths and support professional growth through training, mentorship, and stretch assignments. What career goals are you working toward?",
                "I love helping with career questions! Our paths include technical advancement and management tracks, plus extensive learning opportunities. What aspect of your career development interests you most?",
                "Career growth is a priority here! With our $2000 annual development budget and mentorship programs, there are many ways to advance. What specific guidance do you need?"
            ],
            IntentType.TECHNICAL_SUPPORT: [
                "For technical issues, I recommend checking our troubleshooting guide first, then contacting IT support at it@n3extpath.com if the problem persists. What technical challenge are you facing?",
                "Technical problems can be frustrating! Our IT team is very responsive. For immediate help, try restarting the application or clearing your browser cache. What specific issue do you have?",
                "I can provide basic technical guidance! For complex issues, our IT support team is available. What's not working as expected?"
            ],
            IntentType.GENERAL_HR: [
                "I'm here to help with all HR-related questions! Whether it's policies, processes, benefits, or workplace guidance, I'm your go-to assistant. What can I help you with today?",
                "HR questions are my specialty! From onboarding to career development, benefits to workplace policies, I'm here to support you. What would you like to know?",
                "Great to connect with you! As your HR assistant, I can help with policies, procedures, benefits, and general workplace guidance. How can I assist you?"
            ],
            IntentType.SMALL_TALK: [
                "Hello! I'm your friendly N3EXTPATH HR assistant. I'm here to help with any questions about policies, performance, career development, or workplace guidance. How can I assist you today?",
                "Hi there! Great to chat with you. I'm ready to help with HR questions, policy clarifications, or career guidance. What's on your mind?",
                "Good to hear from you! I'm your HR assistant, here to make your N3EXTPATH experience as smooth as possible. What can I help you with?"
            ]
        }
    
    def _initialize_legendary_responses(self) -> List[str]:
        """Initialize special responses for RICKROLL187"""
        return [
            "🎸 LEGENDARY FOUNDER DETECTED! 🎸 How can I assist the mastermind behind N3EXTPATH today?",
            "🏆 RICKROLL187! The legendary code bro himself! Your Swiss precision leadership continues to inspire. What can I help you with?",
            "💪 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! How can I support the legendary founder today?",
            "⚡ Swiss precision meets legendary fun! RICKROLL187, your leadership made N3EXTPATH the amazing platform it is. How can I assist?",
            "🌟 The legendary founder graces us with his presence! RICKROLL187, your vision of professional excellence with legendary fun guides everything we do. What do you need?",
            "🎸 Code bro energy at maximum! RICKROLL187, your legendary status is permanent. How can I help the master of Swiss precision and legendary jokes?",
            "🚀 LEGENDARY FOUNDER POWER ACTIVATED! The creator of N3EXTPATH needs assistance? I'm honored to help!",
            "💎 RICKROLL187 - the legend, the founder, the code bro! Your legendary vision built this entire platform. What can I do for you today?"
        ]
    
    async def process_message(self, user_id: str, message_content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process incoming chat message and generate response"""
        message_id = str(uuid.uuid4())
        
        # Create user message
        user_message = ChatMessage(
            message_id=message_id,
            user_id=user_id,
            message_type=MessageType.QUESTION,
            content=message_content,
            metadata=context or {}
        )
        
        # Detect intent
        intent, confidence = self._detect_intent(message_content)
        user_message.intent = intent
        user_message.confidence = confidence
        
        # Store in conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        self.conversation_history[user_id].append(user_message)
        
        # Generate response
        response_content = await self._generate_response(user_id, message_content, intent, confidence, context)
        
        # Create response message
        response_message = ChatMessage(
            message_id=str(uuid.uuid4()),
            user_id="ai_assistant",
            message_type=MessageType.LEGENDARY if user_id == "rickroll187" else MessageType.RESPONSE,
            content=response_content,
            intent=intent,
            confidence=confidence,
            metadata={"responding_to": message_id}
        )
        
        self.conversation_history[user_id].append(response_message)
        
        # Limit conversation history
        if len(self.conversation_history[user_id]) > 50:
            self.conversation_history[user_id] = self.conversation_history[user_id][-50:]
        
        return {
            "success": True,
            "message_id": response_message.message_id,
            "response": response_content,
            "intent": intent.value,
            "confidence": round(confidence, 2),
            "timestamp": response_message.timestamp.isoformat(),
            "conversation_id": f"conv_{user_id}_{datetime.utcnow().strftime('%Y%m%d')}",
            "user_type": "legendary_founder" if user_id == "rickroll187" else "employee"
        }
    
    def _detect_intent(self, message: str) -> tuple[IntentType, float]:
        """Detect user intent from message content"""
        message_lower = message.lower()
        intent_scores = {}
        
        # Check each intent pattern
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            
            if score > 0:
                intent_scores[intent_type] = score / len(patterns)
        
        # Special handling for RICKROLL187 mentions
        if any(keyword in message_lower for keyword in ["rickroll187", "legendary", "founder", "code bros"]):
            intent_scores[IntentType.LEGENDARY_INTERACTION] = 1.0
        
        if not intent_scores:
            return IntentType.GENERAL_HR, 0.5
        
        # Return highest scoring intent
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], min(best_intent[1], 1.0)
    
    async def _generate_response(self, user_id: str, message: str, intent: IntentType, confidence: float, context: Dict[str, Any] = None) -> str:
        """Generate appropriate response based on intent and context"""
        
        # Special legendary responses for RICKROLL187
        if user_id == "rickroll187":
            import random
            legendary_response = random.choice(self.legendary_responses)
            
            # Add specific response based on intent
            if intent == IntentType.PERFORMANCE_QUERY:
                specific_response = "Your legendary performance is off the charts! The AI models show you're operating at 120% efficiency with maximum code bro energy!"
            elif intent == IntentType.OKR_HELP:
                specific_response = "Your OKRs are legendary! Building the most professional HR platform while maintaining Swiss precision and code bro fun - that's legendary goal setting!"
            elif intent == IntentType.POLICY_QUESTION:
                specific_response = "As legendary founder, you have access to all policies plus legendary privileges! Your Swiss precision leadership sets the policy standards!"
            else:
                specific_response = "The legendary founder needs assistance? I'm here with Swiss precision and code bro energy!"
            
            return f"{legendary_response}\n\n{specific_response}"
        
        # Standard responses for other users
        if intent in self.response_templates:
            import random
            base_response = random.choice(self.response_templates[intent])
            
            # Add context-specific information
            if intent == IntentType.PERFORMANCE_QUERY and context:
                if context.get("recent_review"):
                    base_response += f"\n\nI see you had a recent review. Your current performance score is looking great!"
            
            elif intent == IntentType.OKR_HELP and context:
                if context.get("current_okrs"):
                    base_response += f"\n\nI can see your current OKRs in the system. Would you like me to help you update progress or create new ones?"
            
            # Add helpful follow-up suggestions
            follow_ups = self._get_follow_up_suggestions(intent)
            if follow_ups:
                base_response += f"\n\n{follow_ups}"
            
            return base_response
        
        # Fallback response
        return "I'm here to help with any HR questions you might have! Feel free to ask about policies, performance, career development, OKRs, or anything else work-related. How can I assist you today?"
    
    def _get_follow_up_suggestions(self, intent: IntentType) -> str:
        """Get follow-up suggestions based on intent"""
        suggestions = {
            IntentType.PERFORMANCE_QUERY: "💡 **Quick tips:** Check your performance dashboard, schedule regular 1:1s with your manager, or explore skill development opportunities.",
            IntentType.OKR_HELP: "💡 **Pro tip:** Make your objectives specific and measurable. Need help writing SMART goals?",
            IntentType.POLICY_QUESTION: "💡 **More info:** Check our employee handbook or ask me about specific policies like vacation, remote work, or benefits.",
            IntentType.CAREER_GUIDANCE: "💡 **Next steps:** Consider scheduling a career planning session with your manager or exploring our learning platform.",
            IntentType.TECHNICAL_SUPPORT: "💡 **Quick fixes:** Try refreshing your browser, clearing cache, or restarting the app. Still stuck? Contact IT support!"
        }
        
        return suggestions.get(intent, "")
    
    async def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """Get conversation summary for user"""
        if user_id not in self.conversation_history:
            return {"success": False, "message": "No conversation history found"}
        
        messages = self.conversation_history[user_id]
        
        # Analyze conversation patterns
        intent_counts = {}
        total_messages = len([m for m in messages if m.message_type == MessageType.QUESTION])
        
        for message in messages:
            if message.intent and message.message_type == MessageType.QUESTION:
                intent_counts[message.intent.value] = intent_counts.get(message.intent.value, 0) + 1
        
        # Get most common topics
        top_topics = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "success": True,
            "user_id": user_id,
            "total_messages": total_messages,
            "conversation_start": messages[0].timestamp.isoformat() if messages else None,
            "last_activity": messages[-1].timestamp.isoformat() if messages else None,
            "top_topics": [{"topic": topic, "count": count} for topic, count in top_topics],
            "is_legendary_user": user_id == "rickroll187",
            "summary": f"Active conversation with {total_messages} questions covering {len(intent_counts)} different topics."
        }
    
    async def get_knowledge_base_info(self, category: str = None) -> Dict[str, Any]:
        """Get information from knowledge base"""
        if category and category in self.knowledge_base:
            return {
                "success": True,
                "category": category,
                "information": self.knowledge_base[category]
            }
        
        return {
            "success": True,
            "available_categories": list(self.knowledge_base.keys()),
            "knowledge_base": self.knowledge_base
        }

# Global chat assistant instance
legendary_chat_assistant = LegendaryChatAssistant()
