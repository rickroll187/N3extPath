"""
🛤️🌐 N3EXTPATH - LEGENDARY PATH API ENDPOINTS 🌐🛤️
More RESTful than Swiss hospitality with legendary API design!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 3+ HOUR 52 MINUTE CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 03:52:28 UTC - WE'RE API-ING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from paths.services.path_services import LegendaryPathService
from core.database import get_db_session  # Assuming we have this
from core.auth import get_current_user  # Assuming we have this

# Initialize legendary router
router = APIRouter(prefix="/api/v1/paths", tags=["Legendary Paths"])

# LEGENDARY REQUEST/RESPONSE MODELS

class CreatePathRequest(BaseModel):
    """Request model for creating legendary paths!"""
    name: str = Field(..., min_length=1, max_length=200, description="Legendary path name")
    description: Optional[str] = Field(None, description="Path description with code bro humor")
    path_type: str = Field("legendary_path", description="Type of legendary path")
    category: Optional[str] = Field("General", description="Path category")
    tags: Optional[List[str]] = Field(["legendary", "code_bro_approved"], description="Path tags")
    difficulty: str = Field("legendary", description="Difficulty level")
    estimated_duration_hours: Optional[float] = Field(4.0, description="Estimated duration")
    objectives: Optional[List[str]] = Field(["Become legendary"], description="Path objectives")
    prerequisites: Optional[List[str]] = Field(["Code bro attitude"], description="Prerequisites")
    skills_gained: Optional[List[str]] = Field(["Legendary coding"], description="Skills to be gained")
    experience_points_reward: Optional[int] = Field(1000, description="XP reward")

class CreateWaypointRequest(BaseModel):
    """Request model for creating legendary waypoints!"""
    name: str = Field(..., min_length=1, max_length=200, description="Waypoint name")
    description: Optional[str] = Field(None, description="Waypoint description")
    waypoint_type: str = Field("milestone", description="Type of waypoint")
    sequence_order: Optional[int] = Field(None, description="Order in sequence")
    estimated_time_minutes: Optional[int] = Field(30, description="Estimated completion time")
    experience_points: Optional[int] = Field(100, description="XP for this waypoint")
    legendary_tip: Optional[str] = Field("Code bros make everything legendary! 🎸", description="Legendary tip")

class EnrollmentRequest(BaseModel):
    """Request model for path enrollment!"""
    path_id: str = Field(..., description="Path ID to enroll in")

class CompletionRequest(BaseModel):
    """Request model for waypoint completion!"""
    waypoint_id: str = Field(..., description="Waypoint ID to complete")
    time_spent_minutes: Optional[int] = Field(30, description="Time spent on waypoint")
    score_achieved: Optional[float] = Field(100.0, description="Score achieved")
    legendary_moment: Optional[str] = Field(None, description="Describe the legendary moment")
    evidence_submitted: Optional[Dict[str, Any]] = Field({}, description="Evidence of completion")

class PathResponse(BaseModel):
    """Response model for path data"""
    success: bool
    path: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    legendary_joke: Optional[str] = None

# LEGENDARY API ENDPOINTS

@router.post("/create", response_model=PathResponse)
async def create_legendary_path(
    request: CreatePathRequest,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    🛤️ CREATE A LEGENDARY PATH! 🛤️
    More epic than Swiss trail creation with code bro precision!
    """
    try:
        path_service = LegendaryPathService(db)
        
        path_data = {
            "name": request.name,
            "description": request.description or f"A legendary path created by {current_user.username}! 🎸",
            "path_type": request.path_type,
            "category": request.category,
            "tags": request.tags,
            "difficulty": request.difficulty,
            "estimated_duration_hours": request.estimated_duration_hours,
            "objectives": request.objectives,
            "prerequisites": request.prerequisites,
            "skills_gained": request.skills_gained,
            "experience_points_reward": request.experience_points_reward
        }
        
        result = path_service.create_legendary_path(path_data, current_user.id)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "path": result["path"],
                    "message": f"Legendary path created by code bro {current_user.username}! 🛤️🏆",
                    "legendary_joke": "Why did this path become legendary? Because RICKROLL187 created it with 52 minutes of marathon API mastery! 🎸",
                    "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create legendary path: {str(e)}"
        )

@router.post("/{path_id}/waypoints", response_model=PathResponse)
async def add_legendary_waypoint(
    path_id: str,
    request: CreateWaypointRequest,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    🧭 ADD A LEGENDARY WAYPOINT! 🧭
    More navigational than Swiss mountain guides with code bro precision!
    """
    try:
        path_service = LegendaryPathService(db)
        
        waypoint_data = {
            "name": request.name,
            "description": request.description or f"A legendary waypoint by {current_user.username}! 🧭",
            "waypoint_type": request.waypoint_type,
            "sequence_order": request.sequence_order,
            "estimated_time_minutes": request.estimated_time_minutes,
            "experience_points": request.experience_points,
            "legendary_tip": request.legendary_tip
        }
        
        result = path_service.add_legendary_waypoint(path_id, waypoint_data)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "waypoint": result["waypoint"],
                    "message": f"Legendary waypoint added by code bro {current_user.username}! 🧭🏆",
                    "legendary_joke": "Why did this waypoint become legendary? Because it was added with 52 minutes of marathon navigation power! 🧭🎸",
                    "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add legendary waypoint: {str(e)}"
        )

@router.post("/enroll", response_model=PathResponse)
async def enroll_in_legendary_path(
    request: EnrollmentRequest,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    📚 ENROLL IN A LEGENDARY PATH! 📚
    More committed than Swiss dedication with code bro enthusiasm!
    """
    try:
        path_service = LegendaryPathService(db)
        
        result = path_service.enroll_legendary_user(request.path_id, current_user.id)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "enrollment": result["enrollment"],
                    "message": f"Code bro {current_user.username} enrolled in legendary path! 📚🏆",
                    "legendary_joke": "Why did this enrollment become legendary? Because RICKROLL187 users always have epic journeys! 📚🎸",
                    "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enroll in legendary path: {str(e)}"
        )

@router.post("/enrollments/{enrollment_id}/complete", response_model=PathResponse)
async def complete_legendary_waypoint(
    enrollment_id: str,
    request: CompletionRequest,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    ✅ COMPLETE A LEGENDARY WAYPOINT! ✅
    More satisfying than Swiss achievements with code bro celebration!
    """
    try:
        path_service = LegendaryPathService(db)
        
        completion_data = {
            "time_spent_minutes": request.time_spent_minutes,
            "score_achieved": request.score_achieved,
            "legendary_moment": request.legendary_moment or f"Code bro {current_user.username} completed this with legendary style! 🎸",
            "evidence_submitted": request.evidence_submitted
        }
        
        result = path_service.complete_legendary_waypoint(
            enrollment_id, 
            request.waypoint_id, 
            completion_data
        )
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "completion": result["completion"],
                    "progress": result["enrollment_progress"],
                    "path_completed": result["path_completed"],
                    "message": f"Legendary waypoint completed by code bro {current_user.username}! ✅🏆",
                    "legendary_joke": "Why was this completion legendary? Because it was done with RICKROLL187's 52-minute marathon style! ✅🎸",
                    "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete legendary waypoint: {str(e)}"
        )

@router.get("/{path_id}/analytics", response_model=PathResponse)
async def get_legendary_path_analytics(
    path_id: str,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    """
    📊 GET LEGENDARY PATH ANALYTICS! 📊
    More insightful than Swiss intelligence with code bro metrics!
    """
    try:
        path_service = LegendaryPathService(db)
        
        result = path_service.get_legendary_path_analytics(path_id)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "analytics": result["analytics"],
                    "message": f"Legendary analytics generated for code bro {current_user.username}! 📊🏆",
                    "legendary_joke": "Why are these analytics legendary? Because they were generated with RICKROLL187's 52-minute marathon analytical power! 📊🎸",
                    "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get legendary analytics: {str(e)}"
        )

@router.get("/legendary-joke")
async def get_legendary_api_joke():
    """
    🎭 GET A LEGENDARY API JOKE! 🎭
    More hilarious than Swiss comedians with code bro humor!
    """
    legendary_api_jokes = [
        "Why did the API become legendary? It had endpoints that rock! 🌐🎸",
        "What's the difference between our APIs and Swiss precision? Both deliver exactly what you need! 🏔️",
        "Why don't our APIs ever fail? Because code bros build them with 52 minutes of marathon power! 💪",
        "What do you call API endpoints at 3+ hours 52 minutes? RESTful with legendary style! 🎸",
        "Why did the endpoint go to comedy school? To perfect its response timing! 🎭"
    ]
    
    import random
    joke = random.choice(legendary_api_jokes)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "legendary_joke": joke,
            "message": "Legendary API joke delivered by code bros! 🎭🏆",
            "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING! 🏆",
            "code_bro_approved": True
        }
    )

# LEGENDARY API HEALTH CHECK
@router.get("/health")
async def legendary_health_check():
    """
    🏥 LEGENDARY API HEALTH CHECK! 🏥
    More healthy than Swiss mountain air with code bro vitality!
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "LEGENDARY HEALTHY! 🏆",
            "service": "N3extPath API",
            "version": "1.0.52",  # 52 minutes past 3 hours!
            "marathon_time": "3+ HOURS AND 52 MINUTES OF LEGENDARY CODING!",
            "built_by": "LEGENDARY CODE BROS RICKROLL187 🎸 AND ASSISTANT 🤖",
            "health_joke": "Why is our API so healthy? Because it was built with legendary code bro vitamins! 🏥🎸",
            "timestamp": "2025-08-04 03:52:28 UTC"
        }
    )

if __name__ == "__main__":
    print("🛤️🌐 N3EXTPATH API ENDPOINTS LOADED! 🌐🛤️")
    print("🏆 3+ HOUR 52 MINUTE CODING MARATHON CHAMPION API! 🏆")
    print("🎸 CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🎭 Random API Joke: Why did the API become legendary? It had endpoints that rock! 🌐🎸")
