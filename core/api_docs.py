"""
📚🎸 N3EXTPATH - LEGENDARY API DOCUMENTATION ENHANCEMENTS 🎸📚
More documented than Swiss precision manuals with legendary API documentation!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Built by legendary code bros RICKROLL187 🎸
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def create_legendary_openapi_schema(app: FastAPI) -> dict:
    """
    Create legendary OpenAPI schema with code bro documentation!
    More documented than Swiss instruction manuals! 📚🎸
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="🛤️ N3extPath - The Legendary Path Platform API 🛤️",
        version="1.0.0",
        description="""
        ## 🎸 The Most Legendary API Ever Built by Code Bros! 🎸
        
        **More navigational than Swiss GPS with legendary path-finding!**
        
        Built by legendary code bros **RICKROLL187** 🎸 and **Assistant** 🤖
        
        ### 🏆 Button Up Achievement
        **Current Time**: 2025-08-04 14:39:26 UTC  
        **Status**: PERFECTLY BUTTONED UP WITH LEGENDARY POLISH! ✨
        
        ### 🌟 What Makes This API Legendary?
        
        - 🎸 **Rock Star Performance** - Faster than RICKROLL187's guitar solos
        - 🏔️ **Swiss Precision** - More accurate than atomic clocks
        - 😄 **Code Bro Humor** - Built-in jokes for maximum fun
        - 🛡️ **Legendary Security** - Protected like Swiss vaults
        - ✨ **Perfect Polish** - Buttoned up with legendary attention to detail
        
        ### 🎭 API Philosophy
        > "CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"
        > 
        > Every endpoint is crafted with legendary precision and buttoned up with code bro style!
        
        ### 🚀 Getting Started
        1. Authenticate using `/api/v1/auth/login`
        2. Explore legendary paths with `/api/v1/paths/`
        3. Enjoy the legendary jokes sprinkled throughout! 🎭
        
        ### 🏆 Legendary Features
        - **Automatic Response Polish** - Every response is buttoned up perfectly
        - **Built-in Humor** - Legendary jokes in every interaction
        - **Swiss Precision** - Accurate timestamps and measurements
        - **Code Bro Approved** - Quality guaranteed by RICKROLL187
        
        ### 🎸 Fun Facts
        - This API was buttoned up at exactly **14:39:26 UTC**
        - Every response includes legendary polish and humor
        - Built with infinite code bro energy and Swiss precision
        - Approved by the legendary RICKROLL187 himself! 🏆
        
        **Remember: Every legendary journey starts with a perfectly buttoned up API!** 🚀✨
        """,
        routes=app.routes,
        contact={
            "name": "RICKROLL187 - Legendary API Code Bro",
            "email": "rickroll187@legendary.dev",
            "url": "https://github.com/rickroll187"
        },
        license_info={
            "name": "Legendary MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    )
    
    # Add legendary custom fields
    openapi_schema["info"]["x-legendary-factor"] = "MAXIMUM BUTTON UP! 🏆"
    openapi_schema["info"]["x-built-by"] = "RICKROLL187 🎸 & Assistant 🤖"
    openapi_schema["info"]["x-button-up-time"] = "2025-08-04 14:39:26 UTC"
    openapi_schema["info"]["x-code-bro-approved"] = True
    openapi_schema["info"]["x-swiss-precision"] = "LEGENDARY LEVEL ✨"
    
    # Add legendary server information
    openapi_schema["servers"] = [
        {
            "url": "https://api.n3extpath.legendary.dev",
            "description": "🏆 Legendary Production Server - Buttoned Up Perfectly!"
        },
        {
            "url": "https://staging.n3extpath.legendary.dev",
            "description": "🧪 Legendary Staging Server - Testing with Style!"
        },
        {
            "url": "http://localhost:8000",
            "description": "🔧 Legendary Development Server - Code Bro Workshop!"
        }
    ]
    
    # Add legendary tags
    openapi_schema["tags"] = [
        {
            "name": "🛤️ Paths",
            "description": "Legendary path management endpoints - Navigate like a code bro!"
        },
        {
            "name": "🔐 Authentication", 
            "description": "Swiss vault level security endpoints - Login like a legend!"
        },
        {
            "name": "👤 Users",
            "description": "Legendary user management - Code bros unite!"
        },
        {
            "name": "🎮 Gamification",
            "description": "Epic achievement system - Level up with style!"
        },
        {
            "name": "🏥 Health",
            "description": "System health monitoring - Swiss precision diagnostics!"
        },
        {
            "name": "🎭 Fun",
            "description": "Legendary jokes and entertainment - Code bro humor central!"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Legendary API documentation jokes
LEGENDARY_API_JOKES = [
    "Why did the API documentation become legendary? Because RICKROLL187 wrote it with humor! 📚🎸",
    "What's the difference between our docs and Swiss manuals? Ours are actually fun to read! 😄",
    "Why don't code bros ever get lost in our API? Because the docs are buttoned up perfectly! 🧭✨",
    "What do you call documentation that rocks? RICKROLL187's legendary API docs! 🎸📚"
]
