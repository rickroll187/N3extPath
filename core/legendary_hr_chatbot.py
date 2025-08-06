"""
🤖🎸 N3EXTPATH - LEGENDARY HR AI CHATBOT 🎸🤖
More helpful than Swiss customer service with legendary AI assistance!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Built while RICKROLL187 showers at 2025-08-05 11:12:20 UTC! 🚿
"""

from typing import Dict, Any, List
import random
from datetime import datetime

class LegendaryHRChatbot:
    """
    🤖 THE LEGENDARY HR AI CHATBOT! 🤖
    More helpful than Swiss precision with hungover code bro AI assistance! 🎸🧠
    """
    
    def __init__(self):
        self.shower_time = "2025-08-05 11:12:20 UTC"
        self.name = "LEGENDARY HR BOT"
        self.personality = "Helpful, humorous, and RICKROLL187-approved"
        
        self.hr_responses = {
            "time_off": [
                "🏖️ To request time off, go to your dashboard and click 'Request Time Off'. I'll make sure it gets legendary approval! 🎸",
                "🌴 Time off requests are processed faster than RICKROLL187's guitar solos! Just submit through the portal! 🎸"
            ],
            "payroll": [
                "💰 Payroll questions? Check your pay stub in the mobile app or contact our legendary payroll team! 🎸",
                "💳 Your paycheck is processed with Swiss precision and legendary accuracy every two weeks! 🏆"
            ],
            "benefits": [
                "🏥 Our benefits package is more comprehensive than Swiss healthcare! Check the benefits portal for details! 🎸",
                "⚕️ Benefits include health, dental, vision, and unlimited legendary jokes from RICKROLL187! 😄"
            ],
            "performance": [
                "📊 Performance reviews happen quarterly and are designed to help you reach legendary status! 🏆",
                "🎯 Set goals, track progress, and get feedback from your manager through the performance portal! 🎸"
            ],
            "training": [
                "🎓 Training opportunities are available through our learning portal - become a legendary code bro! 🎸",
                "📚 We offer courses on everything from technical skills to leadership development! 💪"
            ]
        }
        
        self.chatbot_jokes = [
            "Why is our HR chatbot legendary? Because it helps employees with RICKROLL187 precision at 11:12:20 UTC! 🤖🎸",
            "What's more helpful than Swiss customer service? Legendary HR AI assistance after a hungover shower! 🚿🤖",
            "Why don't employees fear HR questions? Because they get legendary chatbot help with perfect timing! 💪🤖",
            "What do you call perfect hungover AI assistance? A RICKROLL187 shower chatbot special! 🎸🚿"
        ]
    
    def process_hr_query(self, user_message: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process HR query with legendary AI assistance!
        More helpful than Swiss precision with code bro AI support! 🤖🎸
        """
        user_message_lower = user_message.lower()
        
        # Determine query type
        query_type = self._classify_query(user_message_lower)
        
        # Get appropriate response
        if query_type in self.hr_responses:
            response = random.choice(self.hr_responses[query_type])
        else:
            response = self._generate_general_response(user_message)
        
        # Add personal touch if user context available
        if user_context and user_context.get("username"):
            username = user_context["username"]
            if username == "rickroll187":
                response += f"\n\n👑 Special message for the legendary {username}: You're the boss, so you probably already know this! 🎸"
            else:
                response += f"\n\nHope this helps, {username}! 🎸"
        
        return {
            "bot_response": response,
            "query_type": query_type,
            "confidence": 0.95,
            "response_time_ms": 42,  # Always legendary speed
            "helpful_links": self._get_helpful_links(query_type),
            "follow_up_suggestions": self._get_follow_up_suggestions(query_type),
            "processed_at": self.shower_time,
            "processed_by": "RICKROLL187's Legendary HR AI Chatbot 🎸🤖",
            "legendary_joke": random.choice(self.chatbot_jokes)
        }
    
    def _classify_query(self, message: str) -> str:
        """Classify the HR query type!"""
        if any(word in message for word in ["time off", "vacation", "sick", "pto"]):
            return "time_off"
        elif any(word in message for word in ["pay", "salary", "payroll", "paycheck"]):
            return "payroll"
        elif any(word in message for word in ["benefits", "insurance", "health", "dental"]):
            return "benefits"
        elif any(word in message for word in ["performance", "review", "feedback", "goals"]):
            return "performance"
        elif any(word in message for word in ["training", "course", "learning", "development"]):
            return "training"
        else:
            return "general"
    
    def _generate_general_response(self, message: str) -> str:
        """Generate general helpful response!"""
        general_responses = [
            "🤖 I'm here to help with all your HR needs! Can you be more specific about what you're looking for? 🎸",
            "🎸 Great question! For detailed assistance, you can also contact our legendary HR team directly! 🤖",
            "💪 I want to make sure I give you the best answer - could you clarify what type of HR help you need? 🏆"
        ]
        return random.choice(general_responses)
    
    def _get_helpful_links(self, query_type: str) -> List[str]:
        """Get helpful links based on query type!"""
        link_map = {
            "time_off": ["/dashboard/time-off", "/policies/pto"],
            "payroll": ["/dashboard/payroll", "/contact/payroll-team"],
            "benefits": ["/benefits/overview", "/benefits/enrollment"],
            "performance": ["/dashboard/performance", "/goals/tracker"],
            "training": ["/learning/catalog", "/training/schedule"],
            "general": ["/help/faq", "/contact/hr-team"]
        }
        return link_map.get(query_type, link_map["general"])
    
    def _get_follow_up_suggestions(self, query_type: str) -> List[str]:
        """Get follow-up question suggestions!"""
        suggestions_map = {
            "time_off": [
                "How do I check my remaining PTO balance?",
                "What's the approval process for time off?",
                "Can I carry over unused vacation days?"
            ],
            "payroll": [
                "How do I update my direct deposit info?", 
                "When is the next payday?",
                "How do I access my tax documents?"
            ],
            "benefits": [
                "How do I enroll in health insurance?",
                "What dental plans are available?",
                "Can I add dependents to my coverage?"
            ],
            "performance": [
                "How often are performance reviews?",
                "How do I set new goals?",
                "Can I request feedback from my manager?"
            ],
            "training": [
                "What courses are required for my role?",
                "How do I enroll in training?",
                "Are there any upcoming workshops?"
            ]
        }
        return suggestions_map.get(query_type, [
            "How can I contact the HR team?",
            "Where can I find company policies?",
            "What other HR services are available?"
        ])

# Global legendary HR chatbot
legendary_hr_chatbot = LegendaryHRChatbot()
