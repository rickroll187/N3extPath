"""
🔥🎸 N3EXTPATH - LEGENDARY API V1 PACKAGE 🎸🔥
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

__version__ = "1.0.0"
__author__ = "RICKROLL187 - The Legendary Code Rock Star"
__created__ = "2025-08-04 17:37:29 UTC"

# 🎸 LEGENDARY V1 IMPORTS
from .path_endpoints import legendary_path_router
from .user_endpoints import legendary_user_router
from .premium_endpoints import legendary_premium_router
from .monitoring_endpoints import legendary_monitoring_router

__all__ = [
    'legendary_path_router',
    'legendary_user_router', 
    'legendary_premium_router',
    'legendary_monitoring_router'
]

# 🎭 LEGENDARY V1 JOKE
def get_v1_joke():
    return "🎸 Why is V1 legendary? Because it's the first version to be approved by RICKROLL187! 🎸"
