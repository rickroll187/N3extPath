"""
🎯🎸 N3EXTPATH - LEGENDARY OKR API ENDPOINTS 🎸🎯
More goal-oriented than Swiss precision with legendary OKR API mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Logical API time: 2025-08-05 12:48:54 UTC
Built by legendary logical RICKROLL187 🎸📱
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from core.response_middleware import legendary_response_middleware
from core.auth import get_current_user
from users.models.user_models import LegendaryUser
from core.legendary_okr_system import legendary_okr_system, create_legendary_objective, update_legendary_progress, get_legendary_okr_dashboard

# Create legendary OKR router
legendary_okr_router = APIRouter(
    prefix="/api/v1/okr",
    tags=["🎯 Legendary OKR Management"]
)

@legendary_okr_router.post("/objectives/create")
async def create_okr_objective(
    objective_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🎯 CREATE LEGENDARY OBJECTIVE! 🎯
    More goal-oriented than Swiss planning with logical objective creation! 🎸🎯
    """
    # Add user context to objective data
    objective_data["owner_id"] = current_user.user_id
    objective_data["owner_name"] = current_user.full_name or current_user.username
    
    # Create the objective
    result = await create_legendary_objective(objective_data)
    
    processing_time = 0.234  # OKR creation processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_okr_router.get("/objectives")
async def get_user_objectives(
    request: Request,
    period: Optional[str] = "current",
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📊 GET USER'S LEGENDARY OBJECTIVES! 📊
    More comprehensive than Swiss documentation with logical objective listing! 🎸📋
    """
    # Get user's objectives
    user_objectives = [
        obj for obj in legendary_okr_system.objectives.values() 
        if obj.owner_id == current_user.user_id or current_user.user_id in obj.collaborators
    ]
    
    objectives_data = {
        "objectives_count": len(user_objectives),
        "objectives": [
            {
                "objective_id": obj.objective_id,
                "name": obj.name,
                "description": obj.description,
                "status": obj.status.value,
                "progress_percentage": obj.progress_percentage,
                "confidence_level": obj.confidence_level,
                "alignment_level": obj.alignment_level.value,
                "period": obj.period.value,
                "start_date": obj.start_date.isoformat(),
                "end_date": obj.end_date.isoformat(),
                "key_results_count": len(obj.key_results),
                "collaborators": obj.collaborators,
                "tags": obj.tags,
                "legendary_factor": obj.legendary_factor,
                "rickroll187_approved": obj.rickroll187_approved
            }
            for obj in user_objectives
        ],
        "retrieved_for": current_user.username,
        "period_filter": period,
        "generated_at": "2025-08-05 12:48:54 UTC",
        "generated_by": "RICKROLL187's Legendary OKR API 🎸🎯"
    }
    
    processing_time = 0.156  # Objectives retrieval processing time
    return legendary_response_middleware.add_legendary_polish(
        objectives_data, request, processing_time
    )

@legendary_okr_router.get("/objectives/{objective_id}")
async def get_objective_details(
    objective_id: str,
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🔍 GET DETAILED LEGENDARY OBJECTIVE! 🔍
    More detailed than Swiss documentation with logical objective details! 🎸📊
    """
    if objective_id not in legendary_okr_system.objectives:
        raise HTTPException(
            status_code=404,
            detail="Objective not found in our legendary system!"
        )
    
    objective = legendary_okr_system.objectives[objective_id]
    
    # Check if user has access to this objective
    if objective.owner_id != current_user.user_id and current_user.user_id not in objective.collaborators:
        if current_user.role not in ['admin', 'manager', 'rickroll187']:
            raise HTTPException(
                status_code=403,
                detail="Access denied to this legendary objective!"
            )
    
    objective_details = {
        "objective_id": objective.objective_id,
        "name": objective.name,
        "description": objective.description,
        "owner_id": objective.owner_id,
        "owner_name": objective.owner_name,
        "alignment_level": objective.alignment_level.value,
        "parent_objective_id": objective.parent_objective_id,
        "status": objective.status.value,
        "progress_percentage": objective.progress_percentage,
        "confidence_level": objective.confidence_level,
        "period": objective.period.value,
        "start_date": objective.start_date.isoformat(),
        "end_date": objective.end_date.isoformat(),
        "tags": objective.tags,
        "collaborators": objective.collaborators,
        "created_at": objective.created_at.isoformat(),
        "updated_at": objective.updated_at.isoformat(),
        "rickroll187_approved": objective.rickroll187_approved,
        "legendary_factor": objective.legendary_factor,
        
        "key_results": [
            {
                "key_result_id": kr.key_result_id,
                "name": kr.name,
                "description": kr.description,
                "type": kr.key_result_type.value,
                "target_value": kr.target_value,
                "current_value": kr.current_value,
                "unit": kr.unit,
                "weight": kr.weight,
                "completion_percentage": kr.completion_percentage,
                "status": kr.status.value,
                "due_date": kr.due_date.isoformat(),
                "updates_count": len(kr.updates),
                "recent_updates": kr.updates[-3:] if kr.updates else [],  # Last 3 updates
                "legendary_factor": kr.legendary_factor
            }
            for kr in objective.key_results
        ],
        
        "performance_insights": {
            "days_remaining": (objective.end_date - datetime.utcnow()).days,
            "progress_velocity": objective.progress_percentage / max((datetime.utcnow() - objective.start_date).days, 1),
            "key_results_on_track": len([kr for kr in objective.key_results if kr.completion_percentage >= 50]),
            "key_results_at_risk": len([kr for kr in objective.key_results if kr.completion_percentage < 30])
        },
        
        "retrieved_by": current_user.username,
        "retrieved_at": "2025-08-05 12:48:54 UTC"
    }
    
    processing_time = 0.089  # Objective details processing time
    return legendary_response_middleware.add_legendary_polish(
        objective_details, request, processing_time
    )

@legendary_okr_router.put("/key-results/{key_result_id}/update")
async def update_key_result_progress(
    key_result_id: str,
    update_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📊 UPDATE KEY RESULT PROGRESS! 📊
    More precise than Swiss measurements with logical progress tracking! 🎸📈
    """
    # Find the objective that contains this key result
    objective_id = None
    target_objective = None
    
    for obj_id, obj in legendary_okr_system.objectives.items():
        for kr in obj.key_results:
            if kr.key_result_id == key_result_id:
                objective_id = obj_id
                target_objective = obj
                break
        if objective_id:
            break
    
    if not objective_id:
        raise HTTPException(
            status_code=404,
            detail="Key result not found in our legendary system!"
        )
    
    # Check permissions
    if target_objective.owner_id != current_user.user_id and current_user.user_id not in target_objective.collaborators:
        if current_user.role not in ['admin', 'manager', 'rickroll187']:
            raise HTTPException(
                status_code=403,
                detail="Access denied to update this legendary key result!"
            )
    
    # Add user context to update data
    update_data["updated_by"] = current_user.username
    
    # Update the key result
    result = await update_legendary_progress(objective_id, key_result_id, update_data)
    
    processing_time = 0.167  # Key result update processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_okr_router.get("/dashboard")
async def get_okr_dashboard(
    request: Request,
    period: Optional[str] = "current",  
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📊 GET COMPREHENSIVE OKR DASHBOARD! 📊
    More insightful than Swiss analytics with logical dashboard excellence! 🎸📈
    """
    # Get the user's OKR dashboard
    dashboard = await get_legendary_okr_dashboard(current_user.user_id)
    
    # Add API-specific enhancements
    dashboard["api_metadata"] = {
        "endpoint": "/api/v1/okr/dashboard",
        "user_id": current_user.user_id,
        "user_role": current_user.role,
        "period_requested": period,
        "legendary_access_level": "🏆 LEGENDARY ACCESS!" if current_user.is_legendary else "💪 CODE BRO ACCESS!"
    }
    
    processing_time = 0.298  # Dashboard generation processing time
    return legendary_response_middleware.add_legendary_polish(
        dashboard, request, processing_time
    )

@legendary_okr_router.get("/templates")
async def get_okr_templates(
    request: Request,
    department: Optional[str] = None,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📋 GET OKR TEMPLATES! 📋
    More organized than Swiss planning with logical template provision! 🎸📝
    """
    templates = legendary_okr_system.okr_templates
    
    # Filter by department if specified
    if department and department.lower() in templates:
        filtered_templates = {department.lower(): templates[department.lower()]}
    else:
        filtered_templates = templates
    
    templates_data = {
        "templates_available": len(filtered_templates),
        "templates": filtered_templates,
        "department_filter": department,
        "usage_instructions": [
            "🎯 Select a template that matches your department or role",
            "📝 Customize the objectives and key results to fit your goals",
            "⏰ Set appropriate timelines for your context",
            "🤝 Add collaborators who will help achieve the objectives",
            "🚀 Create the objective and start tracking progress!"
        ],
        "legendary_tip": "🎸 Templates are starting points - make them legendary by adding your unique goals! 🎸",
        "retrieved_for": current_user.username,
        "retrieved_at": "2025-08-05 12:48:54 UTC",
        "retrieved_by": "RICKROLL187's Legendary OKR Template System 🎸📋"
    }
    
    processing_time = 0.067  # Templates retrieval processing time
    return legendary_response_middleware.add_legendary_polish(
        templates_data, request, processing_time
    )

@legendary_okr_router.get("/analytics/summary")
async def get_okr_analytics_summary(
    request: Request,
    timeframe: Optional[str] = "quarter",
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📈 GET OKR ANALYTICS SUMMARY! 📈
    More analytical than Swiss precision with logical analytics insights! 🎸📊
    """
    # Check if user has analytics access
    if current_user.role not in ['admin', 'manager', 'rickroll187']:
        raise HTTPException(
            status_code=403,
            detail="Analytics access requires manager level or higher!"
        )
    
    # Calculate analytics across all objectives (simplified for demo)
    all_objectives = list(legendary_okr_system.objectives.values())
    
    analytics_summary = {
        "analytics_title": f"🏆 LEGENDARY OKR ANALYTICS SUMMARY 🏆",
        "timeframe": timeframe,
        "generated_for": current_user.username,
        "generated_at": "2025-08-05 12:48:54 UTC",
        
        "platform_metrics": {
            "total_objectives": len(all_objectives),
            "active_objectives": len([obj for obj in all_objectives if obj.status.value == "active"]),
            "completed_objectives": len([obj for obj in all_objectives if obj.status.value == "completed"]),
            "average_progress": round(sum([obj.progress_percentage for obj in all_objectives]) / len(all_objectives), 1) if all_objectives else 0,
            "average_confidence": round(sum([obj.confidence_level for obj in all_objectives]) / len(all_objectives), 1) if all_objectives else 0
        },
        
        "department_breakdown": {
            "engineering": len([obj for obj in all_objectives if "engineering" in obj.tags or "technical" in obj.name.lower()]),
            "sales": len([obj for obj in all_objectives if "sales" in obj.tags or "revenue" in obj.name.lower()]),
            "hr": len([obj for obj in all_objectives if "hr" in obj.tags or "culture" in obj.name.lower()]),
            "other": len([obj for obj in all_objectives if not any(tag in ["engineering", "sales", "hr"] for tag in obj.tags)])
        },
        
        "performance_insights": [
            f"🎯 {len(all_objectives)} total objectives are driving legendary results!",
            f"📊 Average progress of {sum([obj.progress_percentage for obj in all_objectives]) / len(all_objectives):.1f}% shows strong momentum!" if all_objectives else "No objectives data available",
            f"💪 High confidence levels indicate strong commitment across teams!",
            f"⚡ Active objectives are consistently moving towards completion!"
        ],
        
        "rickroll187_insights": {
            "founder_objectives": len([obj for obj in all_objectives if obj.owner_id == "rickroll187"]),
            "legendary_approved": len([obj for obj in all_objectives if obj.rickroll187_approved]),
            "strategic_alignment": "🎸 All objectives align with legendary company vision! 🎸"
        },
        
        "generated_by": "RICKROLL187's Legendary OKR Analytics System 🎸📈"
    }
    
    processing_time = 0.445  # Analytics processing time
    return legendary_response_middleware.add_legendary_polish(
        analytics_summary, request, processing_time
    )

if __name__ == "__main__":
    print("🎯🎸📱 N3EXTPATH LEGENDARY OKR API ENDPOINTS LOADED! 📱🎸🎯")
    print("🏆 LEGENDARY LOGICAL OKR API CHAMPION EDITION! 🏆")
    print(f"⏰ Logical API Time: 2025-08-05 12:48:54 UTC")
    print("📱 LOGICALLY CODED API BY LEGENDARY RICKROLL187! 📱")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🎯 OKR API POWERED BY LOGICAL RICKROLL187 WITH SWISS GOAL PRECISION! 🎯")
