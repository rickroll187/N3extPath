# File: backend/teams/legendary_team_system.py
"""
👥🎸 N3EXTPATH - LEGENDARY TEAM MANAGEMENT SYSTEM 🎸👥
Professional team collaboration with maximum code bro energy
Built: 2025-08-05 23:18:15 UTC by RICKROLL187
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
# 🎸 LEGENDARY TEAM ROUTER 🎸
# =====================================

router = APIRouter(
    prefix="/teams",
    tags=["Legendary Team Management"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient privileges - Need manager+ role or team membership"},
        404: {"description": "Team not found with Swiss precision"},
        409: {"description": "Team conflict - Name already exists or member conflicts"},
    }
)

# =====================================
# 👥 TEAM ENUMS & CONSTANTS 👥
# =====================================

class TeamType(str, Enum):
    DEPARTMENT = "department"
    PROJECT = "project"
    CROSS_FUNCTIONAL = "cross_functional"
    TEMPORARY = "temporary"
    LEGENDARY = "legendary"

class TeamRole(str, Enum):
    MEMBER = "member"
    LEAD = "lead"
    MANAGER = "manager"
    ADMIN = "admin"

class TeamStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    FORMING = "forming"

class CollaborationLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    LEGENDARY = "legendary"

# Code Bro Energy Levels
CODE_BRO_ENERGY_LEVELS = {
    "infinite": {"multiplier": 3.0, "threshold": 95},
    "maximum": {"multiplier": 2.5, "threshold": 85},
    "high": {"multiplier": 2.0, "threshold": 75},
    "good": {"multiplier": 1.5, "threshold": 65},
    "standard": {"multiplier": 1.0, "threshold": 50}
}

LEGENDARY_TEAM_THRESHOLD = 85.0  # Swiss precision threshold for legendary teams

# =====================================
# 📋 LEGENDARY PYDANTIC MODELS 📋
# =====================================

class TeamMemberRequest(BaseModel):
    """Team member addition request"""
    user_id: str = Field(..., description="User ID to add to team")
    role: TeamRole = Field(default=TeamRole.MEMBER, description="Role in team")
    start_date: Optional[datetime] = Field(None, description="Start date (defaults to now)")
    
class TeamCreateRequest(BaseModel):
    """Team creation request"""
    name: str = Field(..., min_length=3, max_length=100, description="Team name")
    description: str = Field(..., min_length=10, max_length=500, description="Team description")
    team_type: TeamType = Field(..., description="Type of team")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    location: Optional[str] = Field(None, max_length=100, description="Team location")
    max_members: Optional[int] = Field(None, ge=2, le=50, description="Maximum team members")
    
    # Team goals and objectives
    mission_statement: Optional[str] = Field(None, max_length=300, description="Team mission")
    primary_goals: List[str] = Field(default=[], max_items=5, description="Primary team goals")
    
    # Collaboration settings
    collaboration_tools: List[str] = Field(default=[], description="Collaboration tools used")
    meeting_frequency: Optional[str] = Field(None, description="Meeting frequency")
    
    # Legendary features
    is_legendary_team: bool = Field(default=False, description="🎸 Legendary team status")
    swiss_precision_standards: bool = Field(default=False, description="⚙️ Swiss precision standards")
    code_bro_energy_focus: bool = Field(default=True, description="💪 Code bro energy focus")
    
    # Initial members
    initial_members: List[TeamMemberRequest] = Field(default=[], description="Initial team members")
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Team name cannot be empty')
        return v.strip()

class TeamUpdateRequest(BaseModel):
    """Team update request"""
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Updated team name")
    description: Optional[str] = Field(None, min_length=10, max_length=500, description="Updated description")
    department: Optional[str] = Field(None, max_length=100, description="Updated department")
    location: Optional[str] = Field(None, max_length=100, description="Updated location")
    max_members: Optional[int] = Field(None, ge=2, le=50, description="Updated max members")
    mission_statement: Optional[str] = Field(None, max_length=300, description="Updated mission")
    primary_goals: Optional[List[str]] = Field(None, max_items=5, description="Updated goals")
    collaboration_tools: Optional[List[str]] = Field(None, description="Updated tools")
    meeting_frequency: Optional[str] = Field(None, description="Updated meeting frequency")
    status: Optional[TeamStatus] = Field(None, description="Updated status")
    is_legendary_team: Optional[bool] = Field(None, description="🎸 Updated legendary status")
    swiss_precision_standards: Optional[bool] = Field(None, description="⚙️ Updated precision standards")

class TeamMemberResponse(BaseModel):
    """Team member response"""
    user_id: str
    username: str
    full_name: str
    email: str
    role_in_team: str
    job_title: Optional[str]
    department: Optional[str]
    joined_at: datetime
    is_active: bool
    is_legendary: bool
    
    # Performance metrics
    code_bro_energy_level: str
    swiss_precision_score: Optional[float]
    collaboration_rating: Optional[float]
    team_contributions: int

class TeamResponse(BaseModel):
    """Team response model"""
    team_id: str
    name: str
    description: str
    team_type: str
    department: Optional[str]
    location: Optional[str]
    status: str
    max_members: Optional[int]
    current_member_count: int
    mission_statement: Optional[str]
    primary_goals: List[str]
    collaboration_tools: List[str]
    meeting_frequency: Optional[str]
    
    # Team leadership
    team_lead: Optional[Dict[str, str]]
    managers: List[Dict[str, str]]
    
    # Members
    members: List[TeamMemberResponse]
    
    # Team metrics
    team_performance_score: float
    code_bro_energy_level: str
    collaboration_level: str
    swiss_precision_score: Optional[float]
    
    # Legendary status
    is_legendary_team: bool
    legendary_achievements: int
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: str

class TeamListResponse(BaseModel):
    """Team list response with pagination"""
    teams: List[TeamResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class TeamAnalyticsResponse(BaseModel):
    """Team analytics response"""
    team_id: str
    team_name: str
    analysis_period: Dict[str, datetime]
    
    # Performance metrics
    team_performance_score: float
    performance_trend: str
    member_satisfaction: Optional[float]
    productivity_score: float
    
    # Collaboration metrics
    code_bro_energy_level: str
    collaboration_frequency: Dict[str, int]
    meeting_effectiveness: Optional[float]
    cross_team_collaboration: int
    
    # Goal achievement
    goals_completed: int
    goals_in_progress: int
    okr_completion_rate: float
    
    # Swiss precision metrics
    swiss_precision_score: Optional[float]
    quality_standards_adherence: float
    process_efficiency: float
    
    # Legendary metrics
    legendary_achievements: int
    legendary_potential: bool
    
    # AI insights
    ai_insights: Dict[str, Any]
    recommendations: List[str]

# =====================================
# 👥 TEAM CRUD OPERATIONS 👥
# =====================================

@router.post("/", response_model=TeamResponse, summary="👥 Create Team")
async def create_team(
    team_data: TeamCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create new team with legendary collaboration features
    """
    try:
        creator_id = current_user.get("user_id")
        creator_role = current_user.get("role")
        creator_username = current_user.get("username")
        
        # Check permissions - managers and above can create teams
        if creator_role not in ["manager", "hr_manager", "admin", "founder"] and creator_username != "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to create teams - requires manager+ role"
            )
        
        # Check if team name already exists
        existing_team = db.execute(
            text("SELECT team_id FROM teams WHERE LOWER(name) = LOWER(:name)"),
            {"name": team_data.name}
        ).fetchone()
        
        if existing_team:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Team name already exists"
            )
        
        # Validate initial members exist
        if team_data.initial_members:
            member_ids = [member.user_id for member in team_data.initial_members]
            valid_members = db.execute(
                text("SELECT COUNT(*) FROM users WHERE user_id = ANY(:user_ids) AND is_active = true"),
                {"user_ids": member_ids}
            ).scalar()
            
            if valid_members != len(member_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more initial members not found or inactive"
                )
        
        # Generate team ID
        team_id = str(uuid.uuid4())
        
        # Calculate initial Swiss precision score
        swiss_precision_score = calculate_team_swiss_precision_score(team_data)
        
        # Create team
        db.execute(
            text("""
                INSERT INTO teams (
                    team_id, name, description, team_type, department, location, status,
                    max_members, mission_statement, primary_goals, collaboration_tools,
                    meeting_frequency, is_legendary, swiss_precision_standards,
                    swiss_precision_score, code_bro_energy_focus, created_by, created_at
                ) VALUES (
                    :team_id, :name, :description, :team_type, :department, :location, 'forming',
                    :max_members, :mission_statement, :primary_goals, :collaboration_tools,
                    :meeting_frequency, :is_legendary, :swiss_precision_standards,
                    :swiss_precision_score, :code_bro_energy_focus, :created_by, :created_at
                )
            """),
            {
                "team_id": team_id,
                "name": team_data.name,
                "description": team_data.description,
                "team_type": team_data.team_type.value,
                "department": team_data.department,
                "location": team_data.location,
                "max_members": team_data.max_members,
                "mission_statement": team_data.mission_statement,
                "primary_goals": json.dumps(team_data.primary_goals),
                "collaboration_tools": json.dumps(team_data.collaboration_tools),
                "meeting_frequency": team_data.meeting_frequency,
                "is_legendary": team_data.is_legendary_team,
                "swiss_precision_standards": team_data.swiss_precision_standards,
                "swiss_precision_score": swiss_precision_score,
                "code_bro_energy_focus": team_data.code_bro_energy_focus,
                "created_by": creator_id,
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        # Add creator as team admin
        db.execute(
            text("""
                INSERT INTO team_members (
                    team_id, user_id, role, joined_at, added_by
                ) VALUES (
                    :team_id, :user_id, 'admin', :joined_at, :added_by
                )
            """),
            {
                "team_id": team_id,
                "user_id": creator_id,
                "role": "admin",
                "joined_at": datetime.now(timezone.utc),
                "added_by": creator_id
            }
        )
        
        # Add initial members
        for member in team_data.initial_members:
            start_date = member.start_date or datetime.now(timezone.utc)
            
            db.execute(
                text("""
                    INSERT INTO team_members (
                        team_id, user_id, role, joined_at, added_by
                    ) VALUES (
                        :team_id, :user_id, :role, :joined_at, :added_by
                    )
                """),
                {
                    "team_id": team_id,
                    "user_id": member.user_id,
                    "role": member.role.value,
                    "joined_at": start_date,
                    "added_by": creator_id
                }
            )
        
        # Update team status to active if we have members
        if team_data.initial_members:
            db.execute(
                text("UPDATE teams SET status = 'active' WHERE team_id = :team_id"),
                {"team_id": team_id}
            )
        
        # Create legendary team metrics if applicable
        if team_data.is_legendary_team or creator_username == "rickroll187":
            await create_legendary_team_metrics(team_id, db)
        
        db.commit()
        
        logger.info(f"👥 Team created: {team_data.name} by {creator_username}")
        
        # Return created team
        return await get_team(team_id, current_user, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error creating team: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create team"
        )

@router.get("/{team_id}", response_model=TeamResponse, summary="👥 Get Team")
async def get_team(
    team_id: str = Path(..., description="Team ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get team details with Swiss precision metrics and code bro energy
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Get team with creator details
        team_result = db.execute(
            text("""
                SELECT t.*, 
                       creator.username as creator_username,
                       creator.first_name as creator_first_name,
                       creator.last_name as creator_last_name
                FROM teams t
                JOIN users creator ON t.created_by = creator.user_id
                WHERE t.team_id = :team_id
            """),
            {"team_id": team_id}
        ).fetchone()
        
        if not team_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team_data = dict(team_result._mapping)
        
        # Check access permissions
        has_access = False
        
        # Check if user is team member
        team_member_check = db.execute(
            text("SELECT role FROM team_members WHERE team_id = :team_id AND user_id = :user_id"),
            {"team_id": team_id, "user_id": current_user_id}
        ).fetchone()
        
        if team_member_check:
            has_access = True
        elif current_role in ["hr_manager", "admin", "founder"] or current_username == "rickroll187":
            has_access = True
        elif current_role == "manager":
            # Check if any team members report to this manager
            manager_access = db.execute(
                text("""
                    SELECT COUNT(*) FROM team_members tm
                    JOIN users u ON tm.user_id = u.user_id
                    WHERE tm.team_id = :team_id AND u.manager_id = :manager_id
                """),
                {"team_id": team_id, "manager_id": current_user_id}
            ).scalar()
            
            if manager_access > 0:
                has_access = True
        
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to view this team"
            )
        
        # Get team members with details
        members_result = db.execute(
            text("""
                SELECT tm.*, u.username, u.email, u.first_name, u.last_name, u.job_title,
                       u.department, u.is_legendary, u.is_active,
                       COALESCE(lm.code_bro_rating, 5) as code_bro_rating,
                       COALESCE(lm.swiss_precision_score, 0) as swiss_precision_score,
                       COALESCE(tc.contribution_count, 0) as team_contributions
                FROM team_members tm
                JOIN users u ON tm.user_id = u.user_id
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                LEFT JOIN (
                    SELECT user_id, COUNT(*) as contribution_count
                    FROM team_contributions
                    WHERE team_id = :team_id
                    GROUP BY user_id
                ) tc ON u.user_id = tc.user_id
                WHERE tm.team_id = :team_id
                ORDER BY tm.role DESC, tm.joined_at
            """),
            {"team_id": team_id}
        ).fetchall()
        
        # Build member responses
        members = []
        team_lead = None
        managers = []
        
        for member in members_result:
            member_data = dict(member._mapping)
            
            # Determine code bro energy level
            code_bro_rating = member_data.get("code_bro_rating", 5)
            if code_bro_rating >= 9:
                code_bro_energy = "infinite"
            elif code_bro_rating >= 8:
                code_bro_energy = "maximum"
            elif code_bro_rating >= 7:
                code_bro_energy = "high"
            elif code_bro_rating >= 6:
                code_bro_energy = "good"
            else:
                code_bro_energy = "standard"
            
            member_response = TeamMemberResponse(
                user_id=str(member_data["user_id"]),
                username=member_data["username"],
                full_name=f"{member_data['first_name']} {member_data['last_name']}",
                email=member_data["email"],
                role_in_team=member_data["role"],
                job_title=member_data.get("job_title"),
                department=member_data.get("department"),
                joined_at=member_data["joined_at"],
                is_active=member_data["is_active"],
                is_legendary=member_data.get("is_legendary", False),
                code_bro_energy_level=code_bro_energy,
                swiss_precision_score=member_data.get("swiss_precision_score"),
                collaboration_rating=None,  # TODO: Calculate from team interactions
                team_contributions=member_data.get("team_contributions", 0)
            )
            
            members.append(member_response)
            
            # Identify team lead and managers
            if member_data["role"] == "lead" and not team_lead:
                team_lead = {
                    "user_id": str(member_data["user_id"]),
                    "name": f"{member_data['first_name']} {member_data['last_name']}",
                    "username": member_data["username"]
                }
            elif member_data["role"] in ["manager", "admin"]:
                managers.append({
                    "user_id": str(member_data["user_id"]),
                    "name": f"{member_data['first_name']} {member_data['last_name']}",
                    "username": member_data["username"],
                    "role": member_data["role"]
                })
        
        # Calculate team metrics
        team_metrics = calculate_team_performance_metrics(team_data, members, db)
        
        # Parse JSON fields
        primary_goals = json.loads(team_data.get("primary_goals") or "[]")
        collaboration_tools = json.loads(team_data.get("collaboration_tools") or "[]")
        
        # Get legendary achievements count
        legendary_achievements = db.execute(
            text("SELECT COUNT(*) FROM team_achievements WHERE team_id = :team_id"),
            {"team_id": team_id}
        ).scalar() or 0
        
        # Build response
        response = TeamResponse(
            team_id=team_data["team_id"],
            name=team_data["name"],
            description=team_data["description"],
            team_type=team_data["team_type"],
            department=team_data.get("department"),
            location=team_data.get("location"),
            status=team_data["status"],
            max_members=team_data.get("max_members"),
            current_member_count=len(members),
            mission_statement=team_data.get("mission_statement"),
            primary_goals=primary_goals,
            collaboration_tools=collaboration_tools,
            meeting_frequency=team_data.get("meeting_frequency"),
            team_lead=team_lead,
            managers=managers,
            members=members,
            team_performance_score=team_metrics["performance_score"],
            code_bro_energy_level=team_metrics["code_bro_energy_level"],
            collaboration_level=team_metrics["collaboration_level"],
            swiss_precision_score=team_data.get("swiss_precision_score"),
            is_legendary_team=team_data.get("is_legendary", False),
            legendary_achievements=legendary_achievements,
            created_at=team_data["created_at"],
            updated_at=team_data.get("updated_at"),
            created_by=f"{team_data['creator_first_name']} {team_data['creator_last_name']} ({team_data['creator_username']})"
        )
        
        logger.info(f"👥 Team retrieved: {team_data['name']} by {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting team: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team"
        )

@router.get("/", response_model=TeamListResponse, summary="👥 List Teams")
async def list_teams(
    department: Optional[str] = Query(None, description="Filter by department"),
    team_type: Optional[TeamType] = Query(None, description="Filter by team type"),
    status: Optional[TeamStatus] = Query(None, description="Filter by status"),
    is_legendary: Optional[bool] = Query(None, description="Filter by legendary status"),
    my_teams_only: bool = Query(False, description="Show only teams I'm a member of"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    List teams with filtering and pagination
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Build base query
        base_query = """
            FROM teams t
            JOIN users creator ON t.created_by = creator.user_id
            LEFT JOIN (
                SELECT team_id, COUNT(*) as member_count
                FROM team_members
                GROUP BY team_id
            ) mc ON t.team_id = mc.team_id
            WHERE 1=1
        """
        
        query_params = {}
        
        # Access control and filtering
        if my_teams_only or (current_role not in ["hr_manager", "admin", "founder"] and current_username != "rickroll187"):
            # Only show teams user is a member of (unless they have elevated privileges)
            base_query += """
                AND EXISTS (
                    SELECT 1 FROM team_members tm 
                    WHERE tm.team_id = t.team_id AND tm.user_id = :current_user_id
                )
            """
            query_params["current_user_id"] = current_user_id
        
        # Apply filters
        if department:
            base_query += " AND t.department = :department"
            query_params["department"] = department
        
        if team_type:
            base_query += " AND t.team_type = :team_type"
            query_params["team_type"] = team_type.value
        
        if status:
            base_query += " AND t.status = :status"
            query_params["status"] = status.value
        
        if is_legendary is not None:
            base_query += " AND t.is_legendary = :is_legendary"
            query_params["is_legendary"] = is_legendary
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}"
        total_count = db.execute(text(count_query), query_params).scalar()
        
        # Calculate pagination
        total_pages = (total_count + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        # Get teams with pagination
        teams_query = f"""
            SELECT t.team_id, t.name, t.description, t.team_type, t.department, t.location,
                   t.status, t.max_members, t.mission_statement, t.is_legendary,
                   t.swiss_precision_score, t.created_at, t.updated_at,
                   creator.username as creator_username,
                   creator.first_name as creator_first_name,
                   creator.last_name as creator_last_name,
                   COALESCE(mc.member_count, 0) as current_member_count
            {base_query}
            ORDER BY t.created_at DESC
            LIMIT :limit OFFSET :offset
        """
        
        query_params.update({
            "limit": page_size,
            "offset": offset
        })
        
        teams_result = db.execute(text(teams_query), query_params).fetchall()
        
        # Build team responses (simplified for list view)
        teams = []
        for team in teams_result:
            team_dict = dict(team._mapping)
            
            # Get team lead info
            team_lead_result = db.execute(
                text("""
                    SELECT u.user_id, u.username, u.first_name, u.last_name
                    FROM team_members tm
                    JOIN users u ON tm.user_id = u.user_id
                    WHERE tm.team_id = :team_id AND tm.role = 'lead'
                    LIMIT 1
                """),
                {"team_id": team_dict["team_id"]}
            ).fetchone()
            
            team_lead = None
            if team_lead_result:
                lead_data = dict(team_lead_result._mapping)
                team_lead = {
                    "user_id": str(lead_data["user_id"]),
                    "name": f"{lead_data['first_name']} {lead_data['last_name']}",
                    "username": lead_data["username"]
                }
            
            # Calculate simplified team metrics
            performance_score = calculate_simplified_team_performance(team_dict["team_id"], db)
            code_bro_energy_level = determine_team_code_bro_energy(team_dict["team_id"], db)
            
            # Get legendary achievements count
            legendary_achievements = db.execute(
                text("SELECT COUNT(*) FROM team_achievements WHERE team_id = :team_id"),
                {"team_id": team_dict["team_id"]}
            ).scalar() or 0
            
            teams.append(TeamResponse(
                team_id=team_dict["team_id"],
                name=team_dict["name"],
                description=team_dict["description"],
                team_type=team_dict["team_type"],
                department=team_dict.get("department"),
                location=team_dict.get("location"),
                status=team_dict["status"],
                max_members=team_dict.get("max_members"),
                current_member_count=team_dict["current_member_count"],
                mission_statement=team_dict.get("mission_statement"),
                primary_goals=[],  # Simplified for list view
                collaboration_tools=[],  # Simplified for list view
                meeting_frequency=None,  # Simplified for list view
                team_lead=team_lead,
                managers=[],  # Simplified for list view
                members=[],  # Simplified for list view
                team_performance_score=performance_score,
                code_bro_energy_level=code_bro_energy_level,
                collaboration_level="medium",  # Default for list view
                swiss_precision_score=team_dict.get("swiss_precision_score"),
                is_legendary_team=team_dict.get("is_legendary", False),
                legendary_achievements=legendary_achievements,
                created_at=team_dict["created_at"],
                updated_at=team_dict.get("updated_at"),
                created_by=f"{team_dict['creator_first_name']} {team_dict['creator_last_name']} ({team_dict['creator_username']})"
            ))
        
        # Build response
        response = TeamListResponse(
            teams=teams,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
        
        logger.info(f"👥 Teams listed by: {current_username} - Page {page}/{total_pages}")
        
        return response
        
    except Exception as e:
        logger.error(f"🚨 Error listing teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list teams"
        )

# =====================================
# 👤 TEAM MEMBER OPERATIONS 👤
# =====================================

@router.post("/{team_id}/members", summary="➕ Add Team Member")
async def add_team_member(
    team_id: str = Path(..., description="Team ID"),
    member_data: TeamMemberRequest = ...,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Add member to team with code bro energy integration
    """
    try:
        current_user_id = current_user.get("user_id")
        current_username = current_user.get("username")
        
        # Check if team exists
        team_result = db.execute(
            text("SELECT name, max_members, status FROM teams WHERE team_id = :team_id"),
            {"team_id": team_id}
        ).fetchone()
        
        if not team_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team_info = dict(team_result._mapping)
        
        # Check permissions (team admin/manager or HR+)
        team_role = db.execute(
            text("SELECT role FROM team_members WHERE team_id = :team_id AND user_id = :user_id"),
            {"team_id": team_id, "user_id": current_user_id}
        ).fetchone()
        
        current_role = current_user.get("role")
        
        if not team_role and current_role not in ["hr_manager", "admin", "founder"] and current_username != "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to add team members"
            )
        
        if team_role and team_role[0] not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team admins and managers can add members"
            )
        
        # Check if user exists and is active
        user_result = db.execute(
            text("SELECT username, first_name, last_name, is_active FROM users WHERE user_id = :user_id"),
            {"user_id": member_data.user_id}
        ).fetchone()
        
        if not user_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_info = dict(user_result._mapping)
        
        if not user_info["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add inactive user to team"
            )
        
        # Check if user is already a team member
        existing_member = db.execute(
            text("SELECT role FROM team_members WHERE team_id = :team_id AND user_id = :user_id"),
            {"team_id": team_id, "user_id": member_data.user_id}
        ).fetchone()
        
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User is already a team member with role: {existing_member[0]}"
            )
        
        # Check max members limit
        if team_info["max_members"]:
            current_count = db.execute(
                text("SELECT COUNT(*) FROM team_members WHERE team_id = :team_id"),
                {"team_id": team_id}
            ).scalar()
            
            if current_count >= team_info["max_members"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Team has reached maximum member limit ({team_info['max_members']})"
                )
        
        # Add team member
        start_date = member_data.start_date or datetime.now(timezone.utc)
        
        db.execute(
            text("""
                INSERT INTO team_members (
                    team_id, user_id, role, joined_at, added_by
                ) VALUES (
                    :team_id, :user_id, :role, :joined_at, :added_by
                )
            """),
            {
                "team_id": team_id,
                "user_id": member_data.user_id,
                "role": member_data.role.value,
                "joined_at": start_date,
                "added_by": current_user_id
            }
        )
        
        # Update team status to active if it was forming
        if team_info["status"] == "forming":
            db.execute(
                text("UPDATE teams SET status = 'active', updated_at = :updated_at WHERE team_id = :team_id"),
                {"team_id": team_id, "updated_at": datetime.now(timezone.utc)}
            )
        
        # Create team activity log
        db.execute(
            text("""
                INSERT INTO team_activities (
                    activity_id, team_id, user_id, activity_type, activity_data, created_at
                ) VALUES (
                    :activity_id, :team_id, :user_id, 'member_added', :activity_data, :created_at
                )
            """),
            {
                "activity_id": str(uuid.uuid4()),
                "team_id": team_id,
                "user_id": current_user_id,
                "activity_data": json.dumps({
                    "added_user_id": member_data.user_id,
                    "added_username": user_info["username"],
                    "role": member_data.role.value,
                    "added_by": current_username
                }),
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        db.commit()
        
        logger.info(f"➕ Team member added: {user_info['username']} to {team_info['name']} by {current_username}")
        
        return {
            "message": f"Successfully added {user_info['username']} to team {team_info['name']}",
            "team_id": team_id,
            "user_id": member_data.user_id,
            "username": user_info["username"],
            "full_name": f"{user_info['first_name']} {user_info['last_name']}",
            "role": member_data.role.value,
            "joined_at": start_date.isoformat(),
            "added_by": current_username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error adding team member: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add team member"
        )

# =====================================
# 📊 TEAM ANALYTICS & INSIGHTS 📊
# =====================================

@router.get("/{team_id}/analytics", response_model=TeamAnalyticsResponse, summary="📊 Team Analytics")
async def get_team_analytics(
    team_id: str = Path(..., description="Team ID"),
    period_start: Optional[datetime] = Query(None, description="Analysis period start"),
    period_end: Optional[datetime] = Query(None, description="Analysis period end"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get comprehensive team analytics with Swiss precision insights
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Set default period if not provided
        if not period_end:
            period_end = datetime.now(timezone.utc)
        if not period_start:
            period_start = period_end - timedelta(days=90)  # Last 90 days
        
        # Check team exists and access permissions
        team_result = db.execute(
            text("SELECT name, is_legendary FROM teams WHERE team_id = :team_id"),
            {"team_id": team_id}
        ).fetchone()
        
        if not team_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team_info = dict(team_result._mapping)
        
        # Check permissions
        team_member = db.execute(
            text("SELECT role FROM team_members WHERE team_id = :team_id AND user_id = :user_id"),
            {"team_id": team_id, "user_id": current_user_id}
        ).fetchone()
        
        if (not team_member and 
            current_role not in ["hr_manager", "admin", "founder"] and 
            current_username != "rickroll187"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to view team analytics"
            )
        
        # Generate comprehensive team analytics
        analytics_data = await generate_team_analytics(team_id, period_start, period_end, db)
        
        # Build response
        response = TeamAnalyticsResponse(
            team_id=team_id,
            team_name=team_info["name"],
            analysis_period={
                "start": period_start,
                "end": period_end
            },
            team_performance_score=analytics_data["performance_score"],
            performance_trend=analytics_data["performance_trend"],
            member_satisfaction=analytics_data["member_satisfaction"],
            productivity_score=analytics_data["productivity_score"],
            code_bro_energy_level=analytics_data["code_bro_energy_level"],
            collaboration_frequency=analytics_data["collaboration_frequency"],
            meeting_effectiveness=analytics_data["meeting_effectiveness"],
            cross_team_collaboration=analytics_data["cross_team_collaboration"],
            goals_completed=analytics_data["goals_completed"],
            goals_in_progress=analytics_data["goals_in_progress"],
            okr_completion_rate=analytics_data["okr_completion_rate"],
            swiss_precision_score=analytics_data["swiss_precision_score"],
            quality_standards_adherence=analytics_data["quality_standards_adherence"],
            process_efficiency=analytics_data["process_efficiency"],
            legendary_achievements=analytics_data["legendary_achievements"],
            legendary_potential=analytics_data["legendary_potential"],
            ai_insights=analytics_data["ai_insights"],
            recommendations=analytics_data["recommendations"]
        )
        
        logger.info(f"📊 Team analytics generated for {team_info['name']} by {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error generating team analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate team analytics"
        )

# =====================================
# 🎸 LEGENDARY TEAM FUNCTIONS 🎸
# =====================================

def calculate_team_swiss_precision_score(team_data: TeamCreateRequest) -> float:
    """
    Calculate Swiss precision score for team setup
    """
    try:
        base_score = 60.0
        
        # Mission and goals clarity
        if team_data.mission_statement and len(team_data.mission_statement) >= 50:
            base_score += 15.0
        
        if len(team_data.primary_goals) >= 2:
            base_score += 10.0
        
        # Team structure and organization
        if team_data.max_members and 3 <= team_data.max_members <= 12:  # Optimal team size
            base_score += 10.0
        
        # Collaboration tools and processes
        if len(team_data.collaboration_tools) >= 2:
            base_score += 5.0
        
        if team_data.meeting_frequency:
            base_score += 5.0
        
        # Swiss precision standards
        if team_data.swiss_precision_standards:
            base_score += 15.0
        
        # Legendary team bonus
        if team_data.is_legendary_team:
            base_score *= 1.1
        
        return min(100.0, base_score)
        
    except Exception as e:
        logger.error(f"🚨 Error calculating team Swiss precision score: {str(e)}")
        return 60.0

def calculate_team_performance_metrics(
    team_data: Dict[str, Any], 
    members: List[TeamMemberResponse], 
    db: Session
) -> Dict[str, Any]:
    """
    Calculate comprehensive team performance metrics
    """
    try:
        metrics = {
            "performance_score": 75.0,
            "code_bro_energy_level": "standard",
            "collaboration_level": "medium"
        }
        
        if not members:
            return metrics
        
        # Calculate average member performance
        legendary_count = sum(1 for member in members if member.is_legendary)
        active_count = sum(1 for member in members if member.is_active)
        
        # Base performance from member quality
        if legendary_count > 0:
            legendary_ratio = legendary_count / len(members)
            metrics["performance_score"] += legendary_ratio * 20
        
        # Activity and engagement factor
        activity_ratio = active_count / len(members) if members else 0
        metrics["performance_score"] *= activity_ratio
        
        # Team size optimization (Swiss precision)
        team_size = len(members)
        if 5 <= team_size <= 9:  # Optimal team size
            metrics["performance_score"] += 10
        elif team_size < 3:
            metrics["performance_score"] -= 15
        elif team_size > 15:
            metrics["performance_score"] -= 10
        
        # Code bro energy level determination
        avg_code_bro_energy = sum([
            {"infinite": 10, "maximum": 8, "high": 6, "good": 4, "standard": 2}.get(member.code_bro_energy_level, 2)
            for member in members
        ]) / len(members)
        
        if avg_code_bro_energy >= 8:
            metrics["code_bro_energy_level"] = "infinite"
        elif avg_code_bro_energy >= 6:
            metrics["code_bro_energy_level"] = "maximum"
        elif avg_code_bro_energy >= 4:
            metrics["code_bro_energy_level"] = "high"
        elif avg_code_bro_energy >= 3:
            metrics["code_bro_energy_level"] = "good"
        else:
            metrics["code_bro_energy_level"] = "standard"
        
        # Collaboration level based on contributions and interactions
        total_contributions = sum(member.team_contributions for member in members)
        if total_contributions > len(members) * 10:
            metrics["collaboration_level"] = "legendary"
        elif total_contributions > len(members) * 5:
            metrics["collaboration_level"] = "high"
        elif total_contributions > len(members) * 2:
            metrics["collaboration_level"] = "medium"
        else:
            metrics["collaboration_level"] = "low"
        
        # Cap performance score
        metrics["performance_score"] = min(100.0, max(0.0, metrics["performance_score"]))
        
        return metrics
        
    except Exception as e:
        logger.error(f"🚨 Error calculating team performance metrics: {str(e)}")
        return {"performance_score": 50.0, "code_bro_energy_level": "standard", "collaboration_level": "medium"}

def calculate_simplified_team_performance(team_id: str, db: Session) -> float:
    """
    Calculate simplified team performance for list views
    """
    try:
        # Get basic team metrics
        result = db.execute(
            text("""
                SELECT 
                    COUNT(tm.user_id) as member_count,
                    AVG(COALESCE(lm.swiss_precision_score, 70)) as avg_precision,
                    AVG(COALESCE(lm.code_bro_rating, 5)) as avg_code_bro
                FROM team_members tm
                JOIN users u ON tm.user_id = u.user_id
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                WHERE tm.team_id = :team_id AND u.is_active = true
            """),
            {"team_id": team_id}
        ).fetchone()
        
        if not result or result[0] == 0:
            return 50.0
        
        member_count, avg_precision, avg_code_bro = result
        
        # Simple performance calculation
        base_score = 50.0
        base_score += (avg_precision - 70) * 0.3  # Precision factor
        base_score += (avg_code_bro - 5) * 5      # Code bro factor
        
        # Team size factor
        if 5 <= member_count <= 9:
            base_score += 10
        elif member_count < 3:
            base_score -= 10
        
        return min(100.0, max(0.0, base_score))
        
    except Exception as e:
        logger.error(f"🚨 Error calculating simplified team performance: {str(e)}")
        return 50.0

def determine_team_code_bro_energy(team_id: str, db: Session) -> str:
    """
    Determine team code bro energy level
    """
    try:
        # Get team member code bro ratings
        result = db.execute(
            text("""
                SELECT AVG(COALESCE(lm.code_bro_rating, 5)) as avg_rating,
                       COUNT(CASE WHEN u.is_legendary THEN 1 END) as legendary_count,
                       COUNT(*) as total_members
                FROM team_members tm
                JOIN users u ON tm.user_id = u.user_id
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                WHERE tm.team_id = :team_id AND u.is_active = true
            """),
            {"team_id": team_id}
        ).fetchone()
        
        if not result or result[2] == 0:
            return "standard"
        
        avg_rating, legendary_count, total_members = result
        legendary_ratio = legendary_count / total_members
        
        # Determine energy level
        if avg_rating >= 9 or legendary_ratio >= 0.5:
            return "infinite"
        elif avg_rating >= 8 or legendary_ratio >= 0.3:
            return "maximum"
        elif avg_rating >= 7:
            return "high"
        elif avg_rating >= 6:
            return "good"
        else:
            return "standard"
        
    except Exception as e:
        logger.error(f"🚨 Error determining team code bro energy: {str(e)}")
        return "standard"

async def create_legendary_team_metrics(team_id: str, db: Session):
    """
    Create legendary metrics tracking for legendary teams
    """
    try:
        db.execute(
            text("""
                INSERT INTO team_metrics (
                    team_id, legendary_status, swiss_precision_enabled, 
                    code_bro_energy_tracking, created_at
                ) VALUES (
                    :team_id, true, true, true, :created_at
                )
            """),
            {
                "team_id": team_id,
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        logger.info(f"🎸 Legendary team metrics created for team: {team_id}")
        
    except Exception as e:
        logger.error(f"🚨 Error creating legendary team metrics: {str(e)}")

async def generate_team_analytics(
    team_id: str,
    period_start: datetime,
    period_end: datetime,
    db: Session
) -> Dict[str, Any]:
    """
    Generate comprehensive team analytics with AI insights
    """
    try:
        analytics = {
            "performance_score": 75.0,
            "performance_trend": "stable",
            "member_satisfaction": None,
            "productivity_score": 70.0,
            "code_bro_energy_level": "standard",
            "collaboration_frequency": {"daily": 0, "weekly": 0, "monthly": 0},
            "meeting_effectiveness": None,
            "cross_team_collaboration": 0,
            "goals_completed": 0,
            "goals_in_progress": 0,
            "okr_completion_rate": 0.0,
            "swiss_precision_score": None,
            "quality_standards_adherence": 80.0,
            "process_efficiency": 75.0,
            "legendary_achievements": 0,
            "legendary_potential": False,
            "ai_insights": {},
            "recommendations": []
        }
        
        # Get team performance data
        performance_data = db.execute(
            text("""
                SELECT 
                    AVG(COALESCE(lm.swiss_precision_score, 70)) as avg_precision,
                    AVG(COALESCE(lm.code_bro_rating, 5)) as avg_code_bro,
                    COUNT(*) as member_count,
                    COUNT(CASE WHEN u.is_legendary THEN 1 END) as legendary_count
                FROM team_members tm
                JOIN users u ON tm.user_id = u.user_id
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                WHERE tm.team_id = :team_id AND u.is_active = true
            """),
            {"team_id": team_id}
        ).fetchone()
        
        if performance_data and performance_data[3] > 0:  # Has members
            avg_precision, avg_code_bro, member_count, legendary_count = performance_data
            
            # Update analytics with real data
            analytics["performance_score"] = min(100.0, avg_precision * 1.1)
            analytics["swiss_precision_score"] = avg_precision
            
            # Code bro energy level
            if avg_code_bro >= 9:
                analytics["code_bro_energy_level"] = "infinite"
            elif avg_code_bro >= 8:
                analytics["code_bro_energy_level"] = "maximum" 
            elif avg_code_bro >= 7:
                analytics["code_bro_energy_level"] = "high"
            elif avg_code_bro >= 6:
                analytics["code_bro_energy_level"] = "good"
            
            # Legendary potential
            legendary_ratio = legendary_count / member_count
            analytics["legendary_potential"] = (
                legendary_ratio >= 0.3 and 
                avg_precision >= 85 and 
                avg_code_bro >= 8
            )
        
        # Get achievements count
        achievements_count = db.execute(
            text("SELECT COUNT(*) FROM team_achievements WHERE team_id = :team_id"),
            {"team_id": team_id}
        ).scalar() or 0
        
        analytics["legendary_achievements"] = achievements_count
        
        # Generate AI insights
        analytics["ai_insights"] = {
            "team_health": "good" if analytics["performance_score"] >= 75 else "needs_attention",
            "code_bro_synergy": "high" if analytics["code_bro_energy_level"] in ["maximum", "infinite"] else "standard",
            "growth_potential": "high" if analytics["legendary_potential"] else "standard",
            "optimization_opportunities": [
                "Enhance Swiss precision practices" if analytics["swiss_precision_score"] and analytics["swiss_precision_score"] < 85 else None,
                "Boost code bro energy through team activities" if analytics["code_bro_energy_level"] == "standard" else None,
                "Consider legendary team certification" if analytics["legendary_potential"] else None
            ]
        }
        
        # Generate recommendations
        recommendations = []
        
        if analytics["performance_score"] < 70:
            recommendations.append("🎯 Focus on team performance improvement through targeted training")
        
        if analytics["code_bro_energy_level"] == "standard":
            recommendations.append("💪 Organize team building activities to boost code bro energy")
        
        if analytics["swiss_precision_score"] and analytics["swiss_precision_score"] < 80:
            recommendations.append("⚙️ Implement Swiss precision standards and quality processes")
        
        if analytics["legendary_potential"]:
            recommendations.append("🏆 Team shows legendary potential - consider advanced challenges")
        
        if achievements_count == 0:
            recommendations.append("🎸 Set team goals to earn legendary achievements")
        
        analytics["recommendations"] = [rec for rec in recommendations if rec]
        
        return analytics
        
    except Exception as e:
        logger.error(f"🚨 Error generating team analytics: {str(e)}")
        return {
            "performance_score": 50.0,
            "performance_trend": "unknown",
            "member_satisfaction": None,
            "productivity_score": 50.0,
            "code_bro_energy_level": "standard",
            "collaboration_frequency": {"daily": 0, "weekly": 0, "monthly": 0},
            "meeting_effectiveness": None,
            "cross_team_collaboration": 0,
            "goals_completed": 0,
            "goals_in_progress": 0,
            "okr_completion_rate": 0.0,
            "swiss_precision_score": None,
            "quality_standards_adherence": 50.0,
            "process_efficiency": 50.0,
            "legendary_achievements": 0,
            "legendary_potential": False,
            "ai_insights": {"error": "Failed to generate insights"},
            "recommendations": ["Unable to generate recommendations - please try again"]
        }

# =====================================
# 🎸 LEGENDARY EXPORTS 🎸
# =====================================

__all__ = ["router"]

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY TEAM MANAGEMENT SYSTEM LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"Team management system loaded at: 2025-08-05 23:18:15 UTC")
    print("👥 Complete team lifecycle management: ACTIVE")
    print("💪 Maximum code bro energy tracking: INFINITE")
    print("📊 Advanced team analytics: OPERATIONAL")
    print("⚙️ Swiss precision team standards: MAXIMUM")
    print("🏆 Legendary team certification: ENABLED")
    print("🤝 Cross-team collaboration features: ACTIVATED")
    print("👑 RICKROLL187 founder team oversight: EXCLUSIVE ACCESS")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
