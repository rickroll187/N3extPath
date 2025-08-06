"""
⚡🎸 N3EXTPATH - LEGENDARY CORE SYSTEMS PACKAGE 🎸⚡
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

__version__ = "1.0.0"
__author__ = "RICKROLL187 - The Legendary Code Rock Star"
__created__ = "2025-08-04 17:37:29 UTC"

# 🎸 LEGENDARY CORE IMPORTS
from .database import get_db, Base, engine
from .auth import get_current_user, create_access_token
from .response_middleware import legendary_response_middleware
from .performance_middleware import legendary_performance_middleware
from .legendary_security import legendary_input_validator
from .legendary_premium_system import legendary_premium_system

__all__ = [
    'get_db',
    'Base', 
    'engine',
    'get_current_user',
    'create_access_token',
    'legendary_response_middleware',
    'legendary_performance_middleware',
    'legendary_input_validator',
    'legendary_premium_system'
]

# 🎭 LEGENDARY CORE JOKE
def get_core_joke():
    return "🎸 Why is our core legendary? Because it powers everything with RICKROLL187 precision! 🎸"
