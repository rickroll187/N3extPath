# File: backend/okr/legendary_okr_system.py
"""
🎯🎸 N3EXTPATH - LEGENDARY OKR MANAGEMENT SYSTEM 🎸🎯
Professional Objectives and Key Results with Swiss precision
Built: 2025-08-05 22:30:18 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, BackgroundTasks
from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text, func
import statistics
import uuid
import json

# Import dependencies
from auth.security import get_current_user, get_legendary_user, verify_rickroll187
from database.connection import get_db_session, db_utils
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

# =====================================
# 🎸 LEGENDARY OKR ROUTER 🎸
# =====================================

router = APIRouter(
    prefix="/okr",
    tags=["Legendary OKR Management"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient privileges"},
        404: {"description": "OKR not found with Swiss precision"},
        422: {"description": "Validation error - Even legends need proper goals!"},
    }
)

# =====================================
# 🎯 OKR ENUMS & CONSTANTS 🎯
# =====================================

class OKRCycle(str, Enum):
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"
    CUSTOM = "custom"

class OKRStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"

class KeyResultType(str, Enum):
    NUMERIC = "numeric"
    PERCENTAGE = "percentage"
    BOOLEAN = "boolean"
    MILESTONE = "milestone"

class KeyResultStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    AT_RISK = "at_risk"
    COMPLETED = "completed"
    EXCEEDED = "exceeded"

# Swiss Precision OKR Standards
SWISS_PRECISION_THRESHOLDS = {
    "legendary": 120.0,    # 120%+ completion
    "excellent": 100.0,    # 100% completion
    "good": 80.0,          # 80%+ completion
    "satisfactory": 70.0,  # 70%+ completion
    "needs_focus": 50.0    # Below 50% needs attention
}

LEGENDARY_OKR_MULTIPLIER = 1.5  # Legendary users get more ambitious targets

# =====================================
# 📋 LEGENDARY PYDANTIC MODELS 📋
# =====================================

class KeyResultRequest(BaseModel):
    """Key result creation request"""
    title: str = Field(..., min_length=10, max_length=200, description="Key result title")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description")
    type: KeyResultType = Field(..., description="Type of key result")
    target_value: float = Field(..., ge=0, description="Target value to achieve")
    unit: str = Field(..., max_length=50, description="Unit of measurement")
    weight: float = Field(default=1.0, ge=0.1, le=5.0, description="Weight/importance (0.1-5.0)")
    due_date: Optional[datetime] = Field(None, description="Due date for this key result")
    
    # Swiss precision settings
    swiss_precision_target: bool = Field(default=False, description="🎸 Swiss precision target")
    legendary_stretch_goal: bool = Field(default=False, description="🏆 Legendary stretch goal")

class KeyResultUpdate(BaseModel):
    """Key result update request"""
    title: Optional[str] = Field(None, min_length=10, max_length=200, description="Updated title")
    description: Optional[str] = Field(None, max_length=500, description="Updated description")
    current_value: Optional[float] = Field(None, ge=0, description="Current progress value")
    status: Optional[KeyResultStatus] = Field(None, description="Current status")
    notes: Optional[str] = Field(None, max_length=1000, description="Progress notes")
    confidence_level: Optional[int] = Field(None, ge=1, le=10, description="Confidence level (1-10)")

class OKRRequest(BaseModel):
    """OKR creation request"""
    title: str = Field(..., min_length=20, max_length=200, description="Objective title")
    description: str = Field(..., min_length=50, max_length=1000, description="Objective description")
    cycle: OKRCycle = Field(..., description="OKR cycle")
    start_date: datetime = Field(..., description="OKR start date")
    end_date: datetime = Field(..., description="OKR end date")
    key_results: List[KeyResultRequest] = Field(..., min_items=2, max_items=5, description="2-5 key results")
    
    # Alignment and collaboration
    aligned_with_okr_id: Optional[str] = Field(None, description="Parent OKR this aligns with")
    team_okr: bool = Field(default=False, description="Team-wide OKR")
    collaborators: List[str] = Field(default=[], description="Collaborator user IDs")
    
    # Legendary features
    is_legendary_okr: bool = Field(default=False, description="🎸 Legendary OKR status")
    swiss_precision_mode: bool = Field(default=False, description="⚙️ Swiss precision mode")
    code_bro_energy_goal: bool = Field(default=False, description="💪 Code bro energy goal")
    
    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v
    
    @validator('key_results')
    def validate_key_results(cls, v):
        if len(v) < 2:
            raise ValueError('Minimum 2 key results required')
        if len(v) > 5:
            raise ValueError('Maximum 5 key results allowed for focus')
        return v

class OKRUpdate(BaseModel):
    """OKR update request"""
    title: Optional[str] = Field(None, min_length=20, max_length=200, description="Updated title")
    description: Optional[str] = Field(None, min_length=50, max_length=1000, description="Updated description")
    status: Optional[OKRStatus] = Field(None, description="Updated status")
    progress_notes: Optional[str] = Field(None, max_length=2000, description="Progress update notes")
    confidence_level: Optional[int] = Field(None, ge=1, le=10, description="Overall confidence (1-10)")

class KeyResultResponse(BaseModel):
    """Key result response model"""
    kr_id: str
    okr_id: str
    title: str
    description: Optional[str]
    type: str
    target_value: float
    current_value: float
    unit: str
    weight: float
    progress_percentage: float
    status: str
    due_date: Optional[datetime]
    notes: Optional[str]
    confidence_level: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Swiss precision metadata
    swiss_precision_target: bool
    legendary_stretch_goal: bool
    precision_score: Optional[float]

class OKRResponse(BaseModel):
    """OKR response model"""
    okr_id: str
    user_id: str
    owner_name: str
    title: str
    description: str
    cycle: str
    status: str
    start_date: datetime
    end_date: datetime
    progress: float
    confidence_level: Optional[int]
    key_results: List[KeyResultResponse]
    
    # Alignment and collaboration
    aligned_with_okr_id: Optional[str]
    aligned_with_title: Optional[str]
    team_okr: bool
    collaborators: List[Dict[str, str]]
    
    # Legendary metadata
    is_legendary_okr: bool
    swiss_precision_mode: bool
    swiss_precision_score: Optional[float]
    code_bro_energy_goal: bool
    code_bro_energy_level: Optional[str]
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

class OKRListResponse(BaseModel):
    """OKR list response with pagination"""
    okrs: List[OKRResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class OKRAnalyticsResponse(BaseModel):
    """OKR analytics response"""
    user_id: Optional[str]
    period_start: datetime
    period_end: datetime
    
    # Progress analytics
    total_okrs: int
    completed_okrs: int
    active_okrs: int
    average_progress: float
    completion_rate: float
    
    # Key result analytics
    total_key_results: int
    completed_key_results: int
    average_kr_progress: float
    
    # Quality metrics
    swiss_precision_score: Optional[float]
    legendary_okrs_count: int
    code_bro_energy_achievements: int
    
    # Trend analysis
    progress_trend: Dict[str, Any]
    confidence_trend: List[float]
    
    # Comparative analytics
    department_comparison: Optional[Dict[str, Any]]
    company_percentile: Optional[float]
    
    # AI insights
    ai_insights: Dict[str, Any]
    recommendations: List[str]

# =====================================
# 🎯 OKR CRUD OPERATIONS 🎯
# =====================================

@router.post("/", response_model=OKRResponse, summary="🎯 Create OKR")
async def create_okr(
    okr_data: OKRRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create OKR with Swiss precision and legendary features
    """
    try:
        user_id = current_user.get("user_id")
        username = current_user.get("username")
        is_legendary = current_user.get("is_legendary", False) or username == "rickroll187"
        
        # Validate aligned OKR if specified
        if okr_data.aligned_with_okr_id:
            aligned_okr = db.execute(
                text("SELECT okr_id, title FROM okrs WHERE okr_id = :okr_id"),
                {"okr_id": okr_data.aligned_with_okr_id}
            ).fetchone()
            
            if not aligned_okr:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Aligned OKR not found"
                )
        
        # Validate collaborators
        if okr_data.collaborators:
            collaborator_check = db.execute(
                text("SELECT COUNT(*) FROM users WHERE user_id = ANY(:user_ids) AND is_active = true"),
                {"user_ids": okr_data.collaborators}
            ).scalar()
            
            if collaborator_check != len(okr_data.collaborators):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more collaborators not found or inactive"
                )
        
        # Check for overlapping OKRs in the same period
        overlapping_okr = db.execute(
            text("""
                SELECT okr_id FROM okrs 
                WHERE user_id = :user_id 
                  AND status = 'active'
                  AND (start_date <= :end_date AND end_date >= :start_date)
            """),
            {
                "user_id": user_id,
                "start_date": okr_data.start_date,
                "end_date": okr_data.end_date
            }
        ).fetchone()
        
        if overlapping_okr:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Overlapping active OKR exists in this period"
            )
        
        # Generate OKR ID
        okr_id = str(uuid.uuid4())
        
        # Calculate Swiss precision score
        swiss_precision_score = calculate_okr_swiss_precision_score(okr_data, is_legendary)
        
        # Create OKR
        db.execute(
            text("""
                INSERT INTO okrs (
                    okr_id, user_id, title, description, cycle, status, start_date, end_date,
                    progress, aligned_with_okr_id, team_okr, is_legendary, swiss_precision_mode,
                    swiss_precision_score, code_bro_energy_goal, created_at
                ) VALUES (
                    :okr_id, :user_id, :title, :description, :cycle, 'active', :start_date, :end_date,
                    0.0, :aligned_with_okr_id, :team_okr, :is_legendary, :swiss_precision_mode,
                    :swiss_precision_score, :code_bro_energy_goal, :created_at
                )
            """),
            {
                "okr_id": okr_id,
                "user_id": user_id,
                "title": okr_data.title,
                "description": okr_data.description,
                "cycle": okr_data.cycle.value,
                "start_date": okr_data.start_date,
                "end_date": okr_data.end_date,
                "aligned_with_okr_id": okr_data.aligned_with_okr_id,
                "team_okr": okr_data.team_okr,
                "is_legendary": okr_data.is_legendary_okr or is_legendary,
                "swiss_precision_mode": okr_data.swiss_precision_mode,
                "swiss_precision_score": swiss_precision_score,
                "code_bro_energy_goal": okr_data.code_bro_energy_goal,
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        # Create key results
        for i, kr_data in enumerate(okr_data.key_results):
            kr_id = str(uuid.uuid4())
            
            # Calculate precision score for key result
            kr_precision_score = calculate_key_result_precision_score(kr_data, is_legendary)
            
            db.execute(
                text("""
                    INSERT INTO key_results (
                        kr_id, okr_id, title, description, type, target_value, current_value,
                        unit, weight, status, due_date, swiss_precision_target,
                        legendary_stretch_goal, precision_score, created_at
                    ) VALUES (
                        :kr_id, :okr_id, :title, :description, :type, :target_value, 0.0,
                        :unit, :weight, 'not_started', :due_date, :swiss_precision_target,
                        :legendary_stretch_goal, :precision_score, :created_at
                    )
                """),
                {
                    "kr_id": kr_id,
                    "okr_id": okr_id,
                    "title": kr_data.title,
                    "description": kr_data.description,
                    "type": kr_data.type.value,
                    "target_value": kr_data.target_value,
                    "unit": kr_data.unit,
                    "weight": kr_data.weight,
                    "due_date": kr_data.due_date,
                    "swiss_precision_target": kr_data.swiss_precision_target,
                    "legendary_stretch_goal": kr_data.legendary_stretch_goal,
                    "precision_score": kr_precision_score,
                    "created_at": datetime.now(timezone.utc)
                }
            )
        
        # Add collaborators
        for collaborator_id in okr_data.collaborators:
            db.execute(
                text("""
                    INSERT INTO okr_collaborators (okr_id, user_id, added_at)
                    VALUES (:okr_id, :user_id, :added_at)
                """),
                {
                    "okr_id": okr_id,
                    "user_id": collaborator_id,
                    "added_at": datetime.now(timezone.utc)
                }
            )
        
        # Update legendary metrics if applicable
        if is_legendary or okr_data.is_legendary_okr:
            await update_legendary_okr_metrics(user_id, okr_id, db)
        
        db.commit()
        
        logger.info(f"🎯 OKR created: {okr_data.title} by {username}")
        
        # Return created OKR
        return await get_okr(okr_id, current_user, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error creating OKR: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create OKR"
        )

@router.get("/{okr_id}", response_model=OKRResponse, summary="📋 Get OKR")
async def get_okr(
    okr_id: str = Path(..., description="OKR ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get OKR with Swiss precision details and key results
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Get OKR with owner and alignment details
        result = db.execute(
            text("""
                SELECT o.*, 
                       owner.username as owner_username,
                       owner.first_name as owner_first_name,
                       owner.last_name as owner_last_name,
                       aligned.title as aligned_title,
                       COALESCE(lm.code_bro_rating, 5) as code_bro_rating
                FROM okrs o
                JOIN users owner ON o.user_id = owner.user_id
                LEFT JOIN okrs aligned ON o.aligned_with_okr_id = aligned.okr_id
                LEFT JOIN legendary_metrics lm ON o.user_id = lm.user_id
                WHERE o.okr_id = :okr_id
            """),
            {"okr_id": okr_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="OKR not found"
            )
        
        okr_data = dict(result._mapping)
        
        # Check access permissions
        if (str(current_user_id) != str(okr_data["user_id"]) and
            current_role not in ["manager", "hr_manager", "admin", "founder"] and
            current_username != "rickroll187"):
            
            # Check if user is a collaborator
            collaborator_check = db.execute(
                text("SELECT user_id FROM okr_collaborators WHERE okr_id = :okr_id AND user_id = :user_id"),
                {"okr_id": okr_id, "user_id": current_user_id}
            ).fetchone()
            
            if not collaborator_check:
                # Check if user's manager
                if current_role == "manager":
                    manager_check = db.execute(
                        text("SELECT user_id FROM users WHERE user_id = :user_id AND manager_id = :manager_id"),
                        {"user_id": okr_data["user_id"], "manager_id": current_user_id}
                    ).fetchone()
                    
                    if not manager_check:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Insufficient privileges to view this OKR"
                        )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient privileges to view this OKR"
                    )
        
        # Get key results
        key_results_query = db.execute(
            text("""
                SELECT * FROM key_results 
                WHERE okr_id = :okr_id 
                ORDER BY weight DESC, created_at
            """),
            {"okr_id": okr_id}
        ).fetchall()
        
        key_results = []
        for kr in key_results_query:
            kr_data = dict(kr._mapping)
            
            # Calculate progress percentage
            progress_percentage = 0.0
            if kr_data["target_value"] > 0:
                progress_percentage = min(100.0, (kr_data["current_value"] / kr_data["target_value"]) * 100)
            
            key_results.append(KeyResultResponse(
                kr_id=kr_data["kr_id"],
                okr_id=kr_data["okr_id"],
                title=kr_data["title"],
                description=kr_data.get("description"),
                type=kr_data["type"],
                target_value=kr_data["target_value"],
                current_value=kr_data["current_value"],
                unit=kr_data["unit"],
                weight=kr_data["weight"],
                progress_percentage=progress_percentage,
                status=kr_data["status"],
                due_date=kr_data.get("due_date"),
                notes=kr_data.get("notes"),
                confidence_level=kr_data.get("confidence_level"),
                created_at=kr_data["created_at"],
                updated_at=kr_data.get("updated_at"),
                swiss_precision_target=kr_data.get("swiss_precision_target", False),
                legendary_stretch_goal=kr_data.get("legendary_stretch_goal", False),
                precision_score=kr_data.get("precision_score")
            ))
        
        # Get collaborators
        collaborators_query = db.execute(
            text("""
                SELECT u.user_id, u.username, u.first_name, u.last_name
                FROM okr_collaborators oc
                JOIN users u ON oc.user_id = u.user_id
                WHERE oc.okr_id = :okr_id
            """),
            {"okr_id": okr_id}
        ).fetchall()
        
        collaborators = []
        for collab in collaborators_query:
            collab_data = dict(collab._mapping)
            collaborators.append({
                "user_id": str(collab_data["user_id"]),
                "name": f"{collab_data['first_name']} {collab_data['last_name']}",
                "username": collab_data["username"]
            })
        
        # Determine code bro energy level
        code_bro_energy_level = "infinite" if okr_data.get("is_legendary") else "standard"
        if okr_data.get("owner_username") == "rickroll187":
            code_bro_energy_level = "infinite"
        elif okr_data.get("code_bro_energy_goal"):
            code_bro_energy_level = "high"
        
        # Build response
        response = OKRResponse(
            okr_id=okr_data["okr_id"],
            user_id=str(okr_data["user_id"]),
            owner_name=f"{okr_data['owner_first_name']} {okr_data['owner_last_name']}",
            title=okr_data["title"],
            description=okr_data["description"],
            cycle=okr_data["cycle"],
            status=okr_data["status"],
            start_date=okr_data["start_date"],
            end_date=okr_data["end_date"],
            progress=okr_data["progress"],
            confidence_level=okr_data.get("confidence_level"),
            key_results=key_results,
            aligned_with_okr_id=okr_data.get("aligned_with_okr_id"),
            aligned_with_title=okr_data.get("aligned_title"),
            team_okr=okr_data.get("team_okr", False),
            collaborators=collaborators,
            is_legendary_okr=okr_data.get("is_legendary", False),
            swiss_precision_mode=okr_data.get("swiss_precision_mode", False),
            swiss_precision_score=okr_data.get("swiss_precision_score"),
            code_bro_energy_goal=okr_data.get("code_bro_energy_goal", False),
            code_bro_energy_level=code_bro_energy_level,
            created_at=okr_data["created_at"],
            updated_at=okr_data.get("updated_at"),
            completed_at=okr_data.get("completed_at")
        )
        
        logger.info(f"📋 OKR retrieved: {okr_id} by {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting OKR: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve OKR"
        )

@router.get("/", response_model=OKRListResponse, summary="📊 List OKRs")
async def list_okrs(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    status: Optional[OKRStatus] = Query(None, description="Filter by status"),
    cycle: Optional[OKRCycle] = Query(None, description="Filter by cycle"),
    is_legendary: Optional[bool] = Query(None, description="Filter by legendary status"),
    team_okr: Optional[bool] = Query(None, description="Filter by team OKRs"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    List OKRs with filtering and pagination
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Build base query
        base_query = """
            FROM okrs o
            JOIN users owner ON o.user_id = owner.user_id
            LEFT JOIN okrs aligned ON o.aligned_with_okr_id = aligned.okr_id
            LEFT JOIN legendary_metrics lm ON o.user_id = lm.user_id
            WHERE 1=1
        """
        
        query_params = {}
        
        # Access control
        if current_role not in ["hr_manager", "admin", "founder"] and current_username != "rickroll187":
            # Users can see their own OKRs, team OKRs, and OKRs they collaborate on
            base_query += """ AND (
                o.user_id = :current_user_id 
                OR o.team_okr = true
                OR EXISTS (
                    SELECT 1 FROM okr_collaborators oc 
                    WHERE oc.okr_id = o.okr_id AND oc.user_id = :current_user_id
                )
            """
            query_params["current_user_id"] = current_user_id
            
            # Managers can see their direct reports' OKRs
            if current_role == "manager":
                base_query += " OR owner.manager_id = :current_user_id"
            
            base_query += ")"
        
        # Apply filters
        if user_id:
            base_query += " AND o.user_id = :user_id"
            query_params["user_id"] = user_id
        
        if status:
            base_query += " AND o.status = :status"
            query_params["status"] = status.value
        
        if cycle:
            base_query += " AND o.cycle = :cycle"
            query_params["cycle"] = cycle.value
        
        if is_legendary is not None:
            base_query += " AND o.is_legendary = :is_legendary"
            query_params["is_legendary"] = is_legendary
        
        if team_okr is not None:
            base_query += " AND o.team_okr = :team_okr"
            query_params["team_okr"] = team_okr
        
        if start_date:
            base_query += " AND o.start_date >= :start_date"
            query_params["start_date"] = start_date
        
        if end_date:
            base_query += " AND o.end_date <= :end_date"
            query_params["end_date"] = end_date
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}"
        total_count = db.execute(text(count_query), query_params).scalar()
        
        # Calculate pagination
        total_pages = (total_count + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        # Get OKRs with pagination
        okrs_query = f"""
            SELECT o.okr_id, o.user_id, o.title, o.description, o.cycle, o.status,
                   o.start_date, o.end_date, o.progress, o.confidence_level,
                   o.team_okr, o.is_legendary, o.swiss_precision_mode, o.swiss_precision_score,
                   o.code_bro_energy_goal, o.created_at, o.updated_at, o.completed_at,
                   owner.username as owner_username,
                   owner.first_name as owner_first_name,
                   owner.last_name as owner_last_name,
                   aligned.title as aligned_title,
                   COALESCE(lm.code_bro_rating, 5) as code_bro_rating
            {base_query}
            ORDER BY o.created_at DESC
            LIMIT :limit OFFSET :offset
        """
        
        query_params.update({
            "limit": page_size,
            "offset": offset
        })
        
        okrs_result = db.execute(text(okrs_query), query_params).fetchall()
        
        # Build OKR responses (simplified for list view)
        okrs = []
        for okr in okrs_result:
            okr_dict = dict(okr._mapping)
            
            # Get key results count and summary
            kr_summary = db.execute(
                text("""
                    SELECT COUNT(*) as total_kr, 
                           SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_kr,
                           AVG(CASE WHEN target_value > 0 THEN (current_value / target_value) * 100 ELSE 0 END) as avg_progress
                    FROM key_results WHERE okr_id = :okr_id
                """),
                {"okr_id": okr_dict["okr_id"]}
            ).fetchone()
            
            kr_data = dict(kr_summary._mapping) if kr_summary else {"total_kr": 0, "completed_kr": 0, "avg_progress": 0}
            
            # Determine code bro energy level
            code_bro_energy_level = "infinite" if okr_dict.get("is_legendary") else "standard"
            if okr_dict.get("owner_username") == "rickroll187":
                code_bro_energy_level = "infinite"
            elif okr_dict.get("code_bro_energy_goal"):
                code_bro_energy_level = "high"
            
            # Create simplified key results for list view
            key_results_simple = [
                KeyResultResponse(
                    kr_id="summary",
                    okr_id=okr_dict["okr_id"],
                    title=f"{kr_data['completed_kr']}/{kr_data['total_kr']} Key Results Completed",
                    description=f"Average Progress: {kr_data['avg_progress']:.1f}%",
                    type="summary",
                    target_value=kr_data["total_kr"],
                    current_value=kr_data["completed_kr"],
                    unit="key results",
                    weight=1.0,
                    progress_percentage=kr_data["avg_progress"] or 0,
                    status="summary",
                    due_date=None,
                    notes=None,
                    confidence_level=None,
                    created_at=okr_dict["created_at"],
                    updated_at=okr_dict.get("updated_at"),
                    swiss_precision_target=False,
                    legendary_stretch_goal=False,
                    precision_score=None
                )
            ]
            
            okrs.append(OKRResponse(
                okr_id=okr_dict["okr_id"],
                user_id=str(okr_dict["user_id"]),
                owner_name=f"{okr_dict['owner_first_name']} {okr_dict['owner_last_name']}",
                title=okr_dict["title"],
                description=okr_dict["description"],
                cycle=okr_dict["cycle"],
                status=okr_dict["status"],
                start_date=okr_dict["start_date"],
                end_date=okr_dict["end_date"],
                progress=okr_dict["progress"],
                confidence_level=okr_dict.get("confidence_level"),
                key_results=key_results_simple,  # Simplified for list view
                aligned_with_okr_id=okr_dict.get("aligned_with_okr_id"),
                aligned_with_title=okr_dict.get("aligned_title"),
                team_okr=okr_dict.get("team_okr", False),
                collaborators=[],  # Simplified for list view
                is_legendary_okr=okr_dict.get("is_legendary", False),
                swiss_precision_mode=okr_dict.get("swiss_precision_mode", False),
                swiss_precision_score=okr_dict.get("swiss_precision_score"),
                code_bro_energy_goal=okr_dict.get("code_bro_energy_goal", False),
                code_bro_energy_level=code_bro_energy_level,
                created_at=okr_dict["created_at"],
                updated_at=okr_dict.get("updated_at"),
                completed_at=okr_dict.get("completed_at")
            ))
        
        # Build response
        response = OKRListResponse(
            okrs=okrs,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
        
        logger.info(f"📊 OKRs listed by: {current_username} - Page {page}/{total_pages}")
        
        return response
        
    except Exception as e:
        logger.error(f"🚨 Error listing OKRs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list OKRs"
        )

# =====================================
# 📈 KEY RESULT OPERATIONS 📈
# =====================================

@router.put("/key-results/{kr_id}", response_model=KeyResultResponse, summary="📈 Update Key Result")
async def update_key_result(
    kr_id: str = Path(..., description="Key Result ID"),
    update_data: KeyResultUpdate = ...,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Update key result progress with Swiss precision tracking
    """
    try:
        current_user_id = current_user.get("user_id")
        current_username = current_user.get("username")
        
        # Get key result and verify permissions
        kr_result = db.execute(
            text("""
                SELECT kr.*, o.user_id as okr_owner_id, o.okr_id, o.title as okr_title
                FROM key_results kr
                JOIN okrs o ON kr.okr_id = o.okr_id
                WHERE kr.kr_id = :kr_id
            """),
            {"kr_id": kr_id}
        ).fetchone()
        
        if not kr_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Key result not found"
            )
        
        kr_data = dict(kr_result._mapping)
        
        # Check permissions (owner or collaborator)
        if str(current_user_id) != str(kr_data["okr_owner_id"]):
            collaborator_check = db.execute(
                text("SELECT user_id FROM okr_collaborators WHERE okr_id = :okr_id AND user_id = :user_id"),
                {"okr_id": kr_data["okr_id"], "user_id": current_user_id}
            ).fetchone()
            
            if not collaborator_check:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges to update this key result"
                )
        
        # Build update fields
        update_fields = []
        update_params = {"kr_id": kr_id}
        
        for field, value in update_data.dict(exclude_unset=True).items():
            if value is not None:
                update_fields.append(f"{field} = :{field}")
                update_params[field] = value
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        # Auto-update status based on progress
        if update_data.current_value is not None:
            current_value = update_data.current_value
            target_value = kr_data["target_value"]
            
            if target_value > 0:
                progress_percentage = (current_value / target_value) * 100
                
                if progress_percentage >= 120:
                    auto_status = "exceeded"
                elif progress_percentage >= 100:
                    auto_status = "completed"
                elif progress_percentage >= 50:
                    auto_status = "in_progress"
                elif current_value > 0:
                    auto_status = "in_progress"
                else:
                    auto_status = "not_started"
                
                # Update status if not explicitly provided
                if not update_data.status:
                    update_fields.append("status = :auto_status")
                    update_params["auto_status"] = auto_status
        
        # Add updated timestamp
        update_fields.append("updated_at = :updated_at")
        update_params["updated_at"] = datetime.now(timezone.utc)
        
        # Execute update
        update_query = f"""
            UPDATE key_results 
            SET {', '.join(update_fields)}
            WHERE kr_id = :kr_id
        """
        
        db.execute(text(update_query), update_params)
        
        # Recalculate OKR progress
        await recalculate_okr_progress(kr_data["okr_id"], db)
        
        db.commit()
        
        logger.info(f"📈 Key result updated: {kr_data['title']} by {current_username}")
        
        # Return updated key result
        updated_kr = db.execute(
            text("SELECT * FROM key_results WHERE kr_id = :kr_id"),
            {"kr_id": kr_id}
        ).fetchone()
        
        updated_kr_data = dict(updated_kr._mapping)
        
        # Calculate progress percentage
        progress_percentage = 0.0
        if updated_kr_data["target_value"] > 0:
            progress_percentage = min(100.0, (updated_kr_data["current_value"] / updated_kr_data["target_value"]) * 100)
        
        return KeyResultResponse(
            kr_id=updated_kr_data["kr_id"],
            okr_id=updated_kr_data["okr_id"],
            title=updated_kr_data["title"],
            description=updated_kr_data.get("description"),
            type=updated_kr_data["type"],
            target_value=updated_kr_data["target_value"],
            current_value=updated_kr_data["current_value"],
            unit=updated_kr_data["unit"],
            weight=updated_kr_data["weight"],
            progress_percentage=progress_percentage,
            status=updated_kr_data["status"],
            due_date=updated_kr_data.get("due_date"),
            notes=updated_kr_data.get("notes"),
            confidence_level=updated_kr_data.get("confidence_level"),
            created_at=updated_kr_data["created_at"],
            updated_at=updated_kr_data.get("updated_at"),
            swiss_precision_target=updated_kr_data.get("swiss_precision_target", False),
            legendary_stretch_goal=updated_kr_data.get("legendary_stretch_goal", False),
            precision_score=updated_kr_data.get("precision_score")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error updating key result: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update key result"
        )

# =====================================
# 📊 OKR ANALYTICS & INSIGHTS 📊
# =====================================

@router.get("/analytics/{user_id}", response_model=OKRAnalyticsResponse, summary="📊 OKR Analytics")
async def get_okr_analytics(
    user_id: str = Path(..., description="User ID for analytics"),
    period_start: Optional[datetime] = Query(None, description="Analysis period start"),
    period_end: Optional[datetime] = Query(None, description="Analysis period end"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get comprehensive OKR analytics with Swiss precision insights
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Set default period if not provided
        if not period_end:
            period_end = datetime.now(timezone.utc)
        if not period_start:
            period_start = period_end - timedelta(days=365)  # Last year
        
        # Check access permissions
        if (str(current_user_id) != user_id and
            current_role not in ["hr_manager", "admin", "founder"] and
            current_username != "rickroll187"):
            # Managers can view their direct reports
            if current_role == "manager":
                direct_report = db.execute(
                    text("SELECT user_id FROM users WHERE user_id = :user_id AND manager_id = :manager_id"),
                    {"user_id": user_id, "manager_id": current_user_id}
                ).fetchone()
                
                if not direct_report:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient privileges to view analytics for this user"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges to view analytics for this user"
                )
        
        # Get user info
        user_info = db.execute(
            text("SELECT username, first_name, last_name, role, department, is_legendary FROM users WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_data = dict(user_info._mapping)
        
        # Get OKR statistics
        okr_stats = db.execute(
            text("""
                SELECT 
                    COUNT(*) as total_okrs,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_okrs,
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_okrs,
                    AVG(progress) as average_progress,
                    AVG(CASE WHEN swiss_precision_score IS NOT NULL THEN swiss_precision_score ELSE 0 END) as avg_swiss_precision,
                    SUM(CASE WHEN is_legendary = true THEN 1 ELSE 0 END) as legendary_okrs_count,
                    SUM(CASE WHEN code_bro_energy_goal = true THEN 1 ELSE 0 END) as code_bro_energy_achievements
                FROM okrs
                WHERE user_id = :user_id
                  AND start_date >= :period_start
                  AND end_date <= :period_end
            """),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end
            }
        ).fetchone()
        
        if not okr_stats or okr_stats[0] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No OKRs found in the specified period"
            )
        
        stats_data = dict(okr_stats._mapping)
        
        # Get key result statistics
        kr_stats = db.execute(
            text("""
                SELECT 
                    COUNT(*) as total_key_results,
                    SUM(CASE WHEN kr.status = 'completed' THEN 1 ELSE 0 END) as completed_key_results,
                    AVG(CASE WHEN kr.target_value > 0 THEN (kr.current_value / kr.target_value) * 100 ELSE 0 END) as avg_kr_progress
                FROM key_results kr
                JOIN okrs o ON kr.okr_id = o.okr_id
                WHERE o.user_id = :user_id
                  AND o.start_date >= :period_start
                  AND o.end_date <= :period_end
            """),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end
            }
        ).fetchone()
        
        kr_data = dict(kr_stats._mapping)
        
        # Calculate completion rate
        completion_rate = 0.0
        if stats_data["total_okrs"] > 0:
            completion_rate = (stats_data["completed_okrs"] / stats_data["total_okrs"]) * 100
        
        # Get progress trend
        progress_trend_data = db.execute(
            text("""
                SELECT 
                    DATE_TRUNC('month', created_at) as month,
                    AVG(progress) as avg_progress,
                    COUNT(*) as okr_count
                FROM okrs
                WHERE user_id = :user_id
                  AND start_date >= :period_start
                  AND end_date <= :period_end
                GROUP BY DATE_TRUNC('month', created_at)
                ORDER BY month
            """),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end
            }
        ).fetchall()
        
        progress_trend = {
            "monthly_progress": [{"month": row[0].isoformat(), "progress": float(row[1]), "count": row[2]} for row in progress_trend_data],
            "trend_direction": "stable"
        }
        
        # Determine trend direction
        if len(progress_trend_data) >= 2:
            first_month_progress = progress_trend_data[0][1]
            last_month_progress = progress_trend_data[-1][1]
            if last_month_progress > first_month_progress + 10:
                progress_trend["trend_direction"] = "improving"
            elif last_month_progress < first_month_progress - 10:
                progress_trend["trend_direction"] = "declining"
        
        # Get confidence trend
        confidence_data = db.execute(
            text("""
                SELECT confidence_level
                FROM okrs
                WHERE user_id = :user_id
                  AND confidence_level IS NOT NULL
                  AND start_date >= :period_start
                  AND end_date <= :period_end
                ORDER BY created_at
            """),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end
            }
        ).fetchall()
        
        confidence_trend = [float(row[0]) for row in confidence_data]
        
        # Generate AI insights
        ai_insights = generate_okr_ai_insights(stats_data, kr_data, user_data, progress_trend)
        
        # Generate recommendations
        recommendations = generate_okr_recommendations(stats_data, kr_data, user_data, ai_insights)
        
        # Build response
        response = OKRAnalyticsResponse(
            user_id=user_id,
            period_start=period_start,
            period_end=period_end,
            total_okrs=stats_data["total_okrs"],
            completed_okrs=stats_data["completed_okrs"],
            active_okrs=stats_data["active_okrs"],
            average_progress=round(float(stats_data["average_progress"] or 0), 2),
            completion_rate=round(completion_rate, 2),
            total_key_results=kr_data["total_key_results"],
            completed_key_results=kr_data["completed_key_results"],
            average_kr_progress=round(float(kr_data["avg_kr_progress"] or 0), 2),
            swiss_precision_score=round(float(stats_data["avg_swiss_precision"] or 0), 2) if stats_data["avg_swiss_precision"] else None,
            legendary_okrs_count=stats_data["legendary_okrs_count"],
            code_bro_energy_achievements=stats_data["code_bro_energy_achievements"],
            progress_trend=progress_trend,
            confidence_trend=confidence_trend,
            department_comparison=None,  # TODO: Implement department comparison
            company_percentile=None,     # TODO: Implement company percentile
            ai_insights=ai_insights,
            recommendations=recommendations
        )
        
        logger.info(f"📊 OKR analytics generated for {user_data['username']} by {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error generating OKR analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate OKR analytics"
        )

# =====================================
# 🎸 LEGENDARY OKR FUNCTIONS 🎸
# =====================================

def calculate_okr_swiss_precision_score(okr_data: OKRRequest, is_legendary: bool = False) -> float:
    """
    Calculate Swiss precision score for OKR with legendary adjustments
    """
    try:
        # Base score calculation
        base_score = 70.0  # Starting score
        
        # Quality of objectives (clarity, measurability)
        if len(okr_data.title) >= 20 and len(okr_data.description) >= 50:
            base_score += 10.0
        
        # Key results quality
        kr_quality_score = 0
        for kr in okr_data.key_results:
            if kr.swiss_precision_target:
                kr_quality_score += 5
            if kr.legendary_stretch_goal:
                kr_quality_score += 3
            if len(kr.title) >= 10:
                kr_quality_score += 2
        
        base_score += min(20.0, kr_quality_score)
        
        # Strategic alignment
        if okr_data.aligned_with_okr_id:
            base_score += 5.0
        
        # Team collaboration
        if okr_data.team_okr or okr_data.collaborators:
            base_score += 5.0
        
        # Swiss precision mode bonus
        if okr_data.swiss_precision_mode:
            base_score += 10.0
        
        # Legendary multiplier
        if is_legendary or okr_data.is_legendary_okr:
            base_score *= 1.1
        
        return min(100.0, base_score)
        
    except Exception as e:
        logger.error(f"🚨 Error calculating OKR Swiss precision score: {str(e)}")
        return 70.0

def calculate_key_result_precision_score(kr_data: KeyResultRequest, is_legendary: bool = False) -> float:
    """
    Calculate precision score for individual key result
    """
    try:
        base_score = 60.0
        
        # Clarity and specificity
        if len(kr_data.title) >= 15:
            base_score += 10.0
        
        if kr_data.description and len(kr_data.description) >= 20:
            base_score += 10.0
        
        # Measurability
        if kr_data.type in [KeyResultType.NUMERIC, KeyResultType.PERCENTAGE]:
            base_score += 15.0
        elif kr_data.type == KeyResultType.MILESTONE:
            base_score += 10.0
        
        # Ambition level
        if kr_data.legendary_stretch_goal:
            base_score += 15.0
        elif kr_data.swiss_precision_target:
            base_score += 10.0
        
        # Due date planning
        if kr_data.due_date:
            base_score += 5.0
        
        # Legendary bonus
        if is_legendary:
            base_score *= 1.1
        
        return min(100.0, base_score)
        
    except Exception as e:
        logger.error(f"🚨 Error calculating key result precision score: {str(e)}")
        return 60.0

async def recalculate_okr_progress(okr_id: str, db: Session):
    """
    Recalculate OKR progress based on key results
    """
    try:
        # Get all key results for this OKR
        key_results = db.execute(
            text("""
                SELECT target_value, current_value, weight, status
                FROM key_results
                WHERE okr_id = :okr_id
            """),
            {"okr_id": okr_id}
        ).fetchall()
        
        if not key_results:
            return
        
        total_weight = 0
        weighted_progress = 0
        
        for kr in key_results:
            kr_data = dict(kr._mapping)
            weight = kr_data["weight"] or 1.0
            
            # Calculate individual KR progress
            kr_progress = 0.0
            if kr_data["target_value"] > 0:
                kr_progress = min(150.0, (kr_data["current_value"] / kr_data["target_value"]) * 100)
            elif kr_data["status"] == "completed":
                kr_progress = 100.0
            elif kr_data["status"] == "exceeded":
                kr_progress = 120.0
            
            weighted_progress += kr_progress * weight
            total_weight += weight
        
        # Calculate final progress
        final_progress = 0.0
        if total_weight > 0:
            final_progress = weighted_progress / total_weight
        
        # Update OKR progress
        db.execute(
            text("""
                UPDATE okrs 
                SET progress = :progress, updated_at = :updated_at
                WHERE okr_id = :okr_id
            """),
            {
                "okr_id": okr_id,
                "progress": final_progress,
                "updated_at": datetime.now(timezone.utc)
            }
        )
        
        # Check if OKR should be marked as completed
        if final_progress >= 100.0:
            completed_kr_count = len([kr for kr in key_results if dict(kr._mapping)["status"] in ["completed", "exceeded"]])
            if completed_kr_count == len(key_results):
                db.execute(
                    text("""
                        UPDATE okrs 
                        SET status = 'completed', completed_at = :completed_at
                        WHERE okr_id = :okr_id AND status = 'active'
                    """),
                    {
                        "okr_id": okr_id,
                        "completed_at": datetime.now(timezone.utc)
                    }
                )
        
        logger.info(f"📊 OKR progress recalculated: {okr_id} -> {final_progress:.1f}%")
        
    except Exception as e:
        logger.error(f"🚨 Error recalculating OKR progress: {str(e)}")

async def update_legendary_okr_metrics(user_id: str, okr_id: str, db: Session):
    """
    Update legendary metrics for OKR achievements
    """
    try:
        # Update legendary metrics
        db.execute(
            text("""
                INSERT INTO legendary_metrics (
                    user_id, okr_count, legendary_okr_count, updated_at
                ) VALUES (
                    :user_id, 1, 1, :updated_at
                ) ON CONFLICT (user_id) DO UPDATE SET
                    okr_count = legendary_metrics.okr_count + 1,
                    legendary_okr_count = legendary_metrics.legendary_okr_count + 1,
                    updated_at = :updated_at
            """),
            {
                "user_id": user_id,
                "updated_at": datetime.now(timezone.utc)
            }
        )
        
        logger.info(f"🎸 Legendary OKR metrics updated for user: {user_id}")
        
    except Exception as e:
        logger.error(f"🚨 Error updating legendary OKR metrics: {str(e)}")

def generate_okr_ai_insights(
    okr_stats: Dict[str, Any],
    kr_stats: Dict[str, Any],
    user_data: Dict[str, Any],
    progress_trend: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate AI insights for OKR performance
    """
    try:
        insights = {
            "performance_assessment": "",
            "key_strengths": [],
            "improvement_opportunities": [],
            "goal_setting_analysis": {},
            "execution_patterns": {},
            "legendary_potential": False
        }
        
        # Performance assessment
        completion_rate = (okr_stats["completed_okrs"] / okr_stats["total_okrs"]) *

      def generate_okr_ai_insights(
    okr_stats: Dict[str, Any],
    kr_stats: Dict[str, Any],
    user_data: Dict[str, Any],
    progress_trend: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate AI insights for OKR performance with Swiss precision
    """
    try:
        insights = {
            "performance_assessment": "",
            "key_strengths": [],
            "improvement_opportunities": [],
            "goal_setting_analysis": {},
            "execution_patterns": {},
            "legendary_potential": False
        }
        
        # Performance assessment
        completion_rate = (okr_stats["completed_okrs"] / okr_stats["total_okrs"]) * 100 if okr_stats["total_okrs"] > 0 else 0
        avg_progress = okr_stats["average_progress"] or 0
        
        if completion_rate >= 90 and avg_progress >= 100:
            insights["performance_assessment"] = "🏆 Exceptional OKR execution with legendary precision!"
        elif completion_rate >= 75 and avg_progress >= 85:
            insights["performance_assessment"] = "⭐ Strong OKR performance with Swiss-level execution"
        elif completion_rate >= 60 and avg_progress >= 70:
            insights["performance_assessment"] = "✅ Solid OKR performance meeting expectations"
        elif completion_rate >= 40:
            insights["performance_assessment"] = "⚠️ OKR execution needs focused improvement"
        else:
            insights["performance_assessment"] = "🚨 OKR performance requires immediate attention"
        
        # Key strengths analysis
        if completion_rate >= 80:
            insights["key_strengths"].append("Excellent goal completion rate")
        
        if avg_progress >= 90:
            insights["key_strengths"].append("Strong progress tracking and execution")
        
        if okr_stats["legendary_okrs_count"] > 0:
            insights["key_strengths"].append("🎸 Legendary goal-setting capabilities")
        
        if okr_stats["code_bro_energy_achievements"] > 0:
            insights["key_strengths"].append("💪 High code bro energy in collaborative goals")
        
        if progress_trend["trend_direction"] == "improving":
            insights["key_strengths"].append("📈 Positive improvement trajectory over time")
        
        # Improvement opportunities
        if completion_rate < 70:
            insights["improvement_opportunities"].append("Focus on completing more OKRs to target")
        
        if avg_progress < 75:
            insights["improvement_opportunities"].append("Improve progress tracking and milestone achievement")
        
        if kr_stats["avg_kr_progress"] < 70:
            insights["improvement_opportunities"].append("Enhance key result definition and measurement")
        
        if progress_trend["trend_direction"] == "declining":
            insights["improvement_opportunities"].append("Address declining performance trend")
        
        # Goal setting analysis
        total_krs = kr_stats["total_key_results"]
        avg_krs_per_okr = total_krs / okr_stats["total_okrs"] if okr_stats["total_okrs"] > 0 else 0
        
        insights["goal_setting_analysis"] = {
            "average_key_results_per_okr": round(avg_krs_per_okr, 1),
            "goal_scope_assessment": "Optimal" if 2 <= avg_krs_per_okr <= 5 else "Too Complex" if avg_krs_per_okr > 5 else "Too Narrow",
            "strategic_focus": "High" if okr_stats["total_okrs"] <= 4 else "Scattered" if okr_stats["total_okrs"] > 8 else "Moderate",
            "ambition_level": "Legendary" if okr_stats["legendary_okrs_count"] > 0 else "Standard"
        }
        
        # Execution patterns
        kr_completion_rate = (kr_stats["completed_key_results"] / kr_stats["total_key_results"]) * 100 if kr_stats["total_key_results"] > 0 else 0
        
        insights["execution_patterns"] = {
            "key_result_completion_rate": round(kr_completion_rate, 1),
            "execution_consistency": "High" if kr_completion_rate >= 80 else "Medium" if kr_completion_rate >= 60 else "Low",
            "progress_tracking_frequency": "Regular" if avg_progress > 0 else "Irregular",
            "swiss_precision_level": "Maximum" if okr_stats.get("avg_swiss_precision", 0) >= 85 else "Standard"
        }
        
        # Legendary potential assessment
        insights["legendary_potential"] = (
            completion_rate >= 85 and
            avg_progress >= 90 and
            okr_stats["legendary_okrs_count"] > 0 and
            progress_trend["trend_direction"] in ["improving", "stable"]
        )
        
        # Special assessment for RICKROLL187
        if user_data.get("username") == "rickroll187":
            insights["founder_assessment"] = {
                "status": "legendary_founder",
                "performance_level": "infinite",
                "swiss_precision": "maximum",
                "code_bro_energy": "infinite",
                "special_note": "👑 Founder-level OKR execution with infinite legendary potential! 👑"
            }
        
        return insights
        
    except Exception as e:
        logger.error(f"🚨 Error generating OKR AI insights: {str(e)}")
        return {"error": "Failed to generate OKR AI insights"}

def generate_okr_recommendations(
    okr_stats: Dict[str, Any],
    kr_stats: Dict[str, Any],
    user_data: Dict[str, Any],
    ai_insights: Dict[str, Any]
) -> List[str]:
    """
    Generate personalized OKR recommendations with Swiss precision
    """
    try:
        recommendations = []
        
        completion_rate = (okr_stats["completed_okrs"] / okr_stats["total_okrs"]) * 100 if okr_stats["total_okrs"] > 0 else 0
        avg_progress = okr_stats["average_progress"] or 0
        
        # Completion rate recommendations
        if completion_rate < 60:
            recommendations.append("🎯 Focus on completing existing OKRs before setting new ones")
            recommendations.append("📋 Review and potentially simplify current key results")
        elif completion_rate >= 90:
            recommendations.append("🏆 Excellent completion rate - consider more ambitious stretch goals")
        
        # Progress tracking recommendations
        if avg_progress < 70:
            recommendations.append("📊 Implement more frequent progress check-ins (weekly recommended)")
            recommendations.append("🔍 Break down key results into smaller, measurable milestones")
        
        # Key result quality recommendations
        kr_completion_rate = (kr_stats["completed_key_results"] / kr_stats["total_key_results"]) * 100 if kr_stats["total_key_results"] > 0 else 0
        if kr_completion_rate < 70:
            recommendations.append("🎪 Improve key result definition - make them more specific and measurable")
        
        # Strategic recommendations
        total_krs = kr_stats["total_key_results"]
        avg_krs_per_okr = total_krs / okr_stats["total_okrs"] if okr_stats["total_okrs"] > 0 else 0
        
        if avg_krs_per_okr > 5:
            recommendations.append("⚡ Consider reducing key results per OKR (3-5 recommended for focus)")
        elif avg_krs_per_okr < 2:
            recommendations.append("🎯 Add more key results to make objectives more measurable")
        
        # Swiss precision recommendations
        if okr_stats.get("avg_swiss_precision", 0) < 80:
            recommendations.append("⚙️ Enable Swiss precision mode for more rigorous goal tracking")
        
        # Legendary recommendations
        if okr_stats["legendary_okrs_count"] == 0 and user_data.get("is_legendary"):
            recommendations.append("🎸 Consider setting legendary stretch goals to maximize impact")
        
        # Code bro energy recommendations
        if okr_stats["code_bro_energy_achievements"] == 0:
            recommendations.append("💪 Include team collaboration goals to boost code bro energy")
        
        # Trend-based recommendations
        trend_direction = ai_insights.get("execution_patterns", {}).get("execution_consistency", "")
        if trend_direction == "Low":
            recommendations.append("📈 Focus on consistent execution - small daily progress beats sporadic efforts")
        
        # Role-specific recommendations
        if user_data.get("role") == "manager":
            recommendations.append("👨‍💼 Consider setting team-wide OKRs to align and motivate your team")
        
        # Special RICKROLL187 recommendations
        if user_data.get("username") == "rickroll187":
            recommendations.append("👑 As legendary founder, consider setting platform-wide strategic OKRs")
            recommendations.append("🎸 Your OKR execution sets the standard for Swiss precision across N3EXTPATH")
        
        # Generic excellence recommendations
        if completion_rate >= 85 and avg_progress >= 90:
            recommendations.append("🌟 Outstanding performance! Share your OKR methodology with the team")
            recommendations.append("🎯 Consider mentoring others in effective goal-setting practices")
        
        return recommendations
        
    except Exception as e:
        logger.error(f"🚨 Error generating OKR recommendations: {str(e)}")
        return ["Unable to generate personalized recommendations at this time"]

# =====================================
# 🎸 LEGENDARY OKR UTILITIES 🎸
# =====================================

class LegendaryOKRUtils:
    """
    Legendary OKR utilities with Swiss precision
    """
    
    @staticmethod
    def calculate_okr_health_score(progress: float, confidence: int, days_remaining: int) -> Dict[str, Any]:
        """Calculate OKR health score with legendary precision"""
        try:
            # Base health score
            health_score = 50.0
            
            # Progress factor (50% weight)
            progress_factor = min(progress, 150) / 150 * 50
            health_score += progress_factor
            
            # Confidence factor (30% weight)
            if confidence:
                confidence_factor = (confidence / 10) * 30
                health_score += confidence_factor
            
            # Time factor (20% weight)
            if days_remaining > 0:
                if progress >= 75:  # On track
                    time_factor = 20
                elif progress >= 50:  # Slightly behind
                    time_factor = 15
                elif progress >= 25:  # Behind
                    time_factor = 10
                else:  # Significantly behind
                    time_factor = 5
                health_score += time_factor
            
            # Determine health status
            if health_score >= 90:
                status = "excellent"
                emoji = "🏆"
            elif health_score >= 75:
                status = "good"
                emoji = "✅"
            elif health_score >= 60:
                status = "at_risk"
                emoji = "⚠️"
            else:
                status = "critical"
                emoji = "🚨"
            
            return {
                "health_score": round(health_score, 1),
                "status": status,
                "emoji": emoji,
                "description": f"{emoji} OKR health: {status.title()}"
            }
            
        except Exception as e:
            logger.error(f"🚨 Error calculating OKR health score: {str(e)}")
            return {"health_score": 0, "status": "unknown", "emoji": "❓", "description": "Unable to calculate health"}
    
    @staticmethod
    def generate_okr_summary_report(okr_data: Dict[str, Any], key_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive OKR summary report"""
        try:
            # Calculate key metrics
            total_krs = len(key_results)
            completed_krs = len([kr for kr in key_results if kr.get("status") == "completed"])
            avg_kr_progress = sum([kr.get("progress_percentage", 0) for kr in key_results]) / total_krs if total_krs > 0 else 0
            
            # Risk assessment
            at_risk_krs = len([kr for kr in key_results if kr.get("status") == "at_risk"])
            risk_level = "high" if at_risk_krs > total_krs * 0.5 else "medium" if at_risk_krs > 0 else "low"
            
            # Timeline analysis
            start_date = okr_data.get("start_date")
            end_date = okr_data.get("end_date")
            current_date = datetime.now(timezone.utc)
            
            if start_date and end_date:
                total_days = (end_date - start_date).days
                elapsed_days = (current_date - start_date).days
                remaining_days = (end_date - current_date).days
                time_progress = (elapsed_days / total_days) * 100 if total_days > 0 else 100
            else:
                time_progress = 0
                remaining_days = 0
            
            return {
                "okr_id": okr_data.get("okr_id"),
                "title": okr_data.get("title"),
                "overall_progress": okr_data.get("progress", 0),
                "key_results_summary": {
                    "total": total_krs,
                    "completed": completed_krs,
                    "completion_rate": round((completed_krs / total_krs) * 100, 1) if total_krs > 0 else 0,
                    "average_progress": round(avg_kr_progress, 1),
                    "at_risk_count": at_risk_krs
                },
                "timeline_analysis": {
                    "time_elapsed_percent": round(time_progress, 1),
                    "days_remaining": max(0, remaining_days),
                    "on_schedule": avg_kr_progress >= time_progress - 10  # Within 10% tolerance
                },
                "risk_assessment": {
                    "level": risk_level,
                    "factors": [
                        f"{at_risk_krs} key results at risk" if at_risk_krs > 0 else "No key results at risk",
                        "Behind schedule" if avg_kr_progress < time_progress - 15 else "On schedule",
                        "Low confidence" if okr_data.get("confidence_level", 10) < 6 else "Good confidence"
                    ]
                },
                "legendary_metrics": {
                    "is_legendary": okr_data.get("is_legendary_okr", False),
                    "swiss_precision_score": okr_data.get("swiss_precision_score"),
                    "code_bro_energy": okr_data.get("code_bro_energy_goal", False)
                }
            }
            
        except Exception as e:
            logger.error(f"🚨 Error generating OKR summary report: {str(e)}")
            return {"error": "Failed to generate summary report"}

# Global OKR utilities instance
okr_utils = LegendaryOKRUtils()

# =====================================
# 🎸 ADDITIONAL OKR ENDPOINTS 🎸
# =====================================

@router.get("/health/{okr_id}", summary="🏥 OKR Health Check")
async def get_okr_health(
    okr_id: str = Path(..., description="OKR ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get OKR health status with Swiss precision monitoring
    """
    try:
        # Get OKR data
        okr_result = db.execute(
            text("""
                SELECT o.*, u.username
                FROM okrs o
                JOIN users u ON o.user_id = u.user_id
                WHERE o.okr_id = :okr_id
            """),
            {"okr_id": okr_id}
        ).fetchone()
        
        if not okr_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="OKR not found"
            )
        
        okr_data = dict(okr_result._mapping)
        
        # Check permissions (simplified for health check)
        current_user_id = current_user.get("user_id")
        if (str(current_user_id) != str(okr_data["user_id"]) and
            current_user.get("role") not in ["manager", "hr_manager", "admin", "founder"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to view OKR health"
            )
        
        # Calculate days remaining
        end_date = okr_data["end_date"]
        current_date = datetime.now(timezone.utc)
        days_remaining = (end_date - current_date).days if end_date else 0
        
        # Calculate health score
        health_info = okr_utils.calculate_okr_health_score(
            progress=okr_data["progress"] or 0,
            confidence=okr_data.get("confidence_level") or 5,
            days_remaining=days_remaining
        )
        
        # Get key results status
        kr_status = db.execute(
            text("""
                SELECT status, COUNT(*) as count
                FROM key_results
                WHERE okr_id = :okr_id
                GROUP BY status
            """),
            {"okr_id": okr_id}
        ).fetchall()
        
        kr_status_summary = {row[0]: row[1] for row in kr_status}
        
        # Build health response
        health_response = {
            "okr_id": okr_id,
            "title": okr_data["title"],
            "owner": okr_data["username"],
            "health_score": health_info["health_score"],
            "health_status": health_info["status"],
            "health_emoji": health_info["emoji"],
            "health_description": health_info["description"],
            "progress": okr_data["progress"] or 0,
            "confidence_level": okr_data.get("confidence_level"),
            "days_remaining": days_remaining,
            "key_results_status": kr_status_summary,
            "risk_factors": [],
            "recommendations": [],
            "legendary_status": {
                "is_legendary": okr_data.get("is_legendary", False),
                "swiss_precision_score": okr_data.get("swiss_precision_score"),
                "code_bro_energy": okr_data.get("code_bro_energy_goal", False)
            },
            "checked_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Add risk factors
        if health_info["health_score"] < 75:
            health_response["risk_factors"].append("Overall health score below 75%")
        
        if days_remaining < 7 and okr_data["progress"] < 80:
            health_response["risk_factors"].append("Less than 7 days remaining with progress < 80%")
        
        if kr_status_summary.get("at_risk", 0) > 0:
            health_response["risk_factors"].append(f"{kr_status_summary['at_risk']} key results marked as at risk")
        
        # Add recommendations
        if health_info["health_score"] < 60:
            health_response["recommendations"].append("🚨 Schedule immediate OKR review and action plan")
        elif health_info["health_score"] < 75:
            health_response["recommendations"].append("⚠️ Increase focus and resources on this OKR")
        
        if days_remaining < 14 and okr_data["progress"] < 70:
            health_response["recommendations"].append("⏰ Consider scope adjustment or timeline extension")
        
        logger.info(f"🏥 OKR health check: {okr_id} - {health_info['status']}")
        
        return health_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error checking OKR health: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check OKR health"
        )

@router.get("/summary/{okr_id}", summary="📋 OKR Summary Report")
async def get_okr_summary_report(
    okr_id: str = Path(..., description="OKR ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Generate comprehensive OKR summary report
    """
    try:
        # Get complete OKR data (reuse existing get_okr function)
        okr_response = await get_okr(okr_id, current_user, db)
        
        # Convert to dict for processing
        okr_dict = okr_response.dict()
        key_results_dict = [kr.dict() for kr in okr_response.key_results]
        
        # Generate summary report
        summary_report = okr_utils.generate_okr_summary_report(okr_dict, key_results_dict)
        
        logger.info(f"📋 OKR summary report generated: {okr_id}")
        
        return summary_report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error generating OKR summary report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate OKR summary report"
        )

# =====================================
# 🎸 LEGENDARY EXPORTS 🎸
# =====================================

__all__ = ["router", "okr_utils"]

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY OKR MANAGEMENT SYSTEM LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"OKR management system loaded at: 2025-08-05 23:13:29 UTC")
    print("🎯 Complete OKR lifecycle management: ACTIVE")
    print("📈 Swiss precision progress tracking: MAXIMUM")
    print("🏥 OKR health monitoring: OPERATIONAL")
    print("📊 Advanced OKR analytics: ENABLED")
    print("⚡ Code bro energy goal tracking: INFINITE")
    print("🏆 Legendary stretch goal support: ACTIVATED")
    print("👑 RICKROLL187 founder OKR features: EXCLUSIVE ACCESS")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
