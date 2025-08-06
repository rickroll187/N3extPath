# File: backend/users/legendary_user_management.py
"""
👥🎸 N3EXTPATH - LEGENDARY USER MANAGEMENT SYSTEM 🎸👥
Professional user CRUD operations with Swiss precision
Built: 2025-08-05 22:22:54 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, BackgroundTasks
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timezone, timedelta
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text, func
import secrets
import uuid

# Import dependencies
from auth.security import get_current_user, get_legendary_user, verify_rickroll187, hash_password
from database.connection import get_db_session, db_utils
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

# =====================================
# 🎸 LEGENDARY USER MANAGEMENT ROUTER 🎸
# =====================================

router = APIRouter(
    prefix="/users",
    tags=["Legendary User Management"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient privileges - Legendary access may be required"},
        404: {"description": "User not found with Swiss precision"},
        409: {"description": "User conflict - Already exists"},
    }
)

# =====================================
# 📋 LEGENDARY PYDANTIC MODELS 📋
# =====================================

class UserCreateRequest(BaseModel):
    """Create user request with legendary support"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=8, description="Strong password")
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Last name")
    role: str = Field(default="employee", max_length=50, description="User role")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    manager_id: Optional[str] = Field(None, description="Manager user ID")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    location: Optional[str] = Field(None, max_length=100, description="Office location")
    hire_date: Optional[datetime] = Field(None, description="Hire date")
    salary: Optional[float] = Field(None, ge=0, description="Annual salary")
    is_legendary: bool = Field(default=False, description="🎸 Legendary user status")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.lower()
    
    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['employee', 'manager', 'hr_manager', 'admin', 'founder']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v

class UserUpdateRequest(BaseModel):
    """Update user request with legendary flexibility"""
    email: Optional[EmailStr] = Field(None, description="Email address")
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="First name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="Last name")
    role: Optional[str] = Field(None, max_length=50, description="User role")
    department: Optional[str] = Field(None, max_length=100, description="Department")
    manager_id: Optional[str] = Field(None, description="Manager user ID")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    job_title: Optional[str] = Field(None, max_length=100, description="Job title")
    location: Optional[str] = Field(None, max_length=100, description="Office location")
    salary: Optional[float] = Field(None, ge=0, description="Annual salary")
    is_active: Optional[bool] = Field(None, description="Active status")
    is_legendary: Optional[bool] = Field(None, description="🎸 Legendary status (admin only)")
    
    @validator('role')
    def validate_role(cls, v):
        if v is None:
            return v
        valid_roles = ['employee', 'manager', 'hr_manager', 'admin', 'founder']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v

class UserResponse(BaseModel):
    """User response model with legendary metadata"""
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    department: Optional[str]
    manager_id: Optional[str]
    phone: Optional[str]
    job_title: Optional[str]
    location: Optional[str]
    hire_date: Optional[datetime]
    salary: Optional[float]
    is_active: bool
    is_legendary: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    # Legendary metadata
    swiss_precision_score: Optional[float] = None
    code_bro_energy: str = "standard"
    legendary_achievements: int = 0

class UserListResponse(BaseModel):
    """User list response with pagination"""
    users: List[UserResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class UserStatsResponse(BaseModel):
    """User statistics response"""
    total_users: int
    active_users: int
    legendary_users: int
    departments: Dict[str, int]
    roles: Dict[str, int]
    recent_registrations: int
    legendary_stats: Dict[str, Any]

class LegendaryUserRequest(BaseModel):
    """Request to grant or revoke legendary status"""
    user_id: str = Field(..., description="User ID to modify")
    grant_legendary: bool = Field(..., description="Grant or revoke legendary status")
    reason: str = Field(..., min_length=10, description="Reason for status change")
    swiss_precision_level: Optional[str] = Field("maximum", description="Swiss precision level")
    code_bro_energy_level: Optional[str] = Field("maximum", description="Code bro energy level")

# =====================================
# 👤 USER CRUD OPERATIONS 👤
# =====================================

@router.get("/me", response_model=UserResponse, summary="👤 Get Current User")
async def get_current_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get current user's complete profile with legendary metadata
    """
    try:
        username = current_user.get("username")
        
        # Get complete user profile
        result = db.execute(
            text("""
                SELECT u.*, 
                       COALESCE(lm.swiss_precision_score, 0) as swiss_precision_score,
                       COALESCE(lm.code_bro_rating, 5) as code_bro_rating,
                       COALESCE(la.achievement_count, 0) as legendary_achievements
                FROM users u
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                LEFT JOIN (
                    SELECT user_id, COUNT(*) as achievement_count 
                    FROM legendary_achievements 
                    GROUP BY user_id
                ) la ON u.user_id = la.user_id
                WHERE u.username = :username
            """),
            {"username": username}
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        user_data = dict(result._mapping)
        
        # Determine code bro energy level
        code_bro_energy = "infinite" if user_data.get("is_legendary") else "standard"
        if username == "rickroll187":
            code_bro_energy = "infinite"
        
        # Build response
        user_response = UserResponse(
            user_id=str(user_data["user_id"]),
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            department=user_data.get("department"),
            manager_id=str(user_data["manager_id"]) if user_data.get("manager_id") else None,
            phone=user_data.get("phone"),
            job_title=user_data.get("job_title"),
            location=user_data.get("location"),
            hire_date=user_data.get("hire_date"),
            salary=user_data.get("salary"),
            is_active=user_data["is_active"],
            is_legendary=user_data.get("is_legendary", False),
            created_at=user_data["created_at"],
            last_login=user_data.get("last_login"),
            swiss_precision_score=user_data.get("swiss_precision_score"),
            code_bro_energy=code_bro_energy,
            legendary_achievements=user_data.get("legendary_achievements", 0)
        )
        
        logger.info(f"👤 Profile retrieved for: {username}")
        
        return user_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )

@router.put("/me", response_model=UserResponse, summary="✏️ Update Current User")
async def update_current_user_profile(
    update_data: UserUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Update current user's profile with legendary precision
    """
    try:
        username = current_user.get("username")
        user_id = current_user.get("user_id")
        
        # Build update fields
        update_fields = []
        update_params = {"user_id": user_id}
        
        for field, value in update_data.dict(exclude_unset=True).items():
            if field == "is_legendary":
                # Only admins and RICKROLL187 can change legendary status
                if current_user.get("role") not in ["admin", "founder"] and username != "rickroll187":
                    continue
            
            if value is not None:
                update_fields.append(f"{field} = :{field}")
                update_params[field] = value
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        # Add updated_at timestamp
        update_fields.append("updated_at = :updated_at")
        update_params["updated_at"] = datetime.now(timezone.utc)
        
        # Execute update
        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE user_id = :user_id
        """
        
        db.execute(text(update_query), update_params)
        db.commit()
        
        logger.info(f"✏️ Profile updated for: {username}")
        
        # Return updated profile
        return await get_current_user_profile(current_user, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error updating user profile: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

@router.get("/", response_model=UserListResponse, summary="👥 List Users")
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or username"),
    department: Optional[str] = Query(None, description="Filter by department"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_legendary: Optional[bool] = Query(None, description="Filter by legendary status"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    List users with filtering and pagination (requires manager+ role)
    """
    try:
        # Check permissions
        user_role = current_user.get("role")
        username = current_user.get("username")
        
        if user_role not in ["manager", "hr_manager", "admin", "founder"] and username != "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to list users"
            )
        
        # Build base query
        base_query = """
            FROM users u
            LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
            LEFT JOIN (
                SELECT user_id, COUNT(*) as achievement_count 
                FROM legendary_achievements 
                GROUP BY user_id
            ) la ON u.user_id = la.user_id
            WHERE 1=1
        """
        
        query_params = {}
        
        # Add filters
        if search:
            base_query += " AND (u.username ILIKE :search OR u.first_name ILIKE :search OR u.last_name ILIKE :search OR u.email ILIKE :search)"
            query_params["search"] = f"%{search}%"
        
        if department:
            base_query += " AND u.department = :department"
            query_params["department"] = department
        
        if role:
            base_query += " AND u.role = :role"
            query_params["role"] = role
        
        if is_active is not None:
            base_query += " AND u.is_active = :is_active"
            query_params["is_active"] = is_active
        
        if is_legendary is not None:
            base_query += " AND u.is_legendary = :is_legendary"
            query_params["is_legendary"] = is_legendary
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}"
        total_count = db.execute(text(count_query), query_params).scalar()
        
        # Calculate pagination
        total_pages = (total_count + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        # Get users with pagination
        users_query = f"""
            SELECT u.*, 
                   COALESCE(lm.swiss_precision_score, 0) as swiss_precision_score,
                   COALESCE(lm.code_bro_rating, 5) as code_bro_rating,
                   COALESCE(la.achievement_count, 0) as legendary_achievements
            {base_query}
            ORDER BY u.created_at DESC
            LIMIT :limit OFFSET :offset
        """
        
        query_params.update({
            "limit": page_size,
            "offset": offset
        })
        
        users_result = db.execute(text(users_query), query_params).fetchall()
        
        # Build user responses
        users = []
        for user_data in users_result:
            user_dict = dict(user_data._mapping)
            
            # Determine code bro energy
            code_bro_energy = "infinite" if user_dict.get("is_legendary") else "standard"
            if user_dict.get("username") == "rickroll187":
                code_bro_energy = "infinite"
            
            users.append(UserResponse(
                user_id=str(user_dict["user_id"]),
                username=user_dict["username"],
                email=user_dict["email"],
                first_name=user_dict["first_name"],
                last_name=user_dict["last_name"],
                role=user_dict["role"],
                department=user_dict.get("department"),
                manager_id=str(user_dict["manager_id"]) if user_dict.get("manager_id") else None,
                phone=user_dict.get("phone"),
                job_title=user_dict.get("job_title"),
                location=user_dict.get("location"),
                hire_date=user_dict.get("hire_date"),
                salary=user_dict.get("salary") if user_role in ["hr_manager", "admin", "founder"] else None,  # Hide salary for non-HR
                is_active=user_dict["is_active"],
                is_legendary=user_dict.get("is_legendary", False),
                created_at=user_dict["created_at"],
                last_login=user_dict.get("last_login"),
                swiss_precision_score=user_dict.get("swiss_precision_score"),
                code_bro_energy=code_bro_energy,
                legendary_achievements=user_dict.get("legendary_achievements", 0)
            ))
        
        # Build response
        response = UserListResponse(
            users=users,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )
        
        logger.info(f"👥 Users listed by: {username} - Page {page}/{total_pages}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error listing users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list users"
        )

@router.get("/{user_id}", response_model=UserResponse, summary="👤 Get User by ID")
async def get_user_by_id(
    user_id: str = Path(..., description="User ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get user by ID with legendary metadata (requires manager+ role or own profile)
    """
    try:
        current_username = current_user.get("username")
        current_role = current_user.get("role")
        current_user_id = current_user.get("user_id")
        
        # Check if user is viewing their own profile or has sufficient privileges
        if (str(current_user_id) != user_id and 
            current_role not in ["manager", "hr_manager", "admin", "founder"] and 
            current_username != "rickroll187"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to view this user"
            )
        
        # Get user profile
        result = db.execute(
            text("""
                SELECT u.*, 
                       COALESCE(lm.swiss_precision_score, 0) as swiss_precision_score,
                       COALESCE(lm.code_bro_rating, 5) as code_bro_rating,
                       COALESCE(la.achievement_count, 0) as legendary_achievements
                FROM users u
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                LEFT JOIN (
                    SELECT user_id, COUNT(*) as achievement_count 
                    FROM legendary_achievements 
                    GROUP BY user_id
                ) la ON u.user_id = la.user_id
                WHERE u.user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_data = dict(result._mapping)
        
        # Determine code bro energy level
        code_bro_energy = "infinite" if user_data.get("is_legendary") else "standard"
        if user_data.get("username") == "rickroll187":
            code_bro_energy = "infinite"
        
        # Build response (hide salary for non-HR roles)
        user_response = UserResponse(
            user_id=str(user_data["user_id"]),
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            department=user_data.get("department"),
            manager_id=str(user_data["manager_id"]) if user_data.get("manager_id") else None,
            phone=user_data.get("phone"),
            job_title=user_data.get("job_title"),
            location=user_data.get("location"),
            hire_date=user_data.get("hire_date"),
            salary=user_data.get("salary") if current_role in ["hr_manager", "admin", "founder"] or str(current_user_id) == user_id else None,
            is_active=user_data["is_active"],
            is_legendary=user_data.get("is_legendary", False),
            created_at=user_data["created_at"],
            last_login=user_data.get("last_login"),
            swiss_precision_score=user_data.get("swiss_precision_score"),
            code_bro_energy=code_bro_energy,
            legendary_achievements=user_data.get("legendary_achievements", 0)
        )
        
        logger.info(f"👤 User profile retrieved: {user_data['username']} by {current_username}")
        
        return user_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting user by ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )

@router.post("/", response_model=UserResponse, summary="➕ Create User")
async def create_user(
    user_data: UserCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create new user (requires admin+ role)
    """
    try:
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Check permissions
        if current_role not in ["admin", "founder"] and current_username != "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to create users"
            )
        
        # Check if username or email already exists
        existing_user = db.execute(
            text("SELECT username FROM users WHERE username = :username OR email = :email"),
            {"username": user_data.username, "email": user_data.email}
        ).fetchone()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists"
            )
        
        # Validate manager_id if provided
        if user_data.manager_id:
            manager_exists = db.execute(
                text("SELECT user_id FROM users WHERE user_id = :manager_id"),
                {"manager_id": user_data.manager_id}
            ).fetchone()
            
            if not manager_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid manager_id"
                )
        
        # Hash password
        hashed_password = hash_password(user_data.password, user_data.is_legendary)
        
        # Generate user ID
        new_user_id = str(uuid.uuid4())
        
        # Create user
        db.execute(
            text("""
                INSERT INTO users (
                    user_id, username, email, password_hash, first_name, last_name,
                    role, department, manager_id, phone, job_title, location, 
                    hire_date, salary, is_active, is_legendary, created_at
                ) VALUES (
                    :user_id, :username, :email, :password_hash, :first_name, :last_name,
                    :role, :department, :manager_id, :phone, :job_title, :location,
                    :hire_date, :salary, true, :is_legendary, :created_at
                )
            """),
            {
                "user_id": new_user_id,
                "username": user_data.username,
                "email": user_data.email,
                "password_hash": hashed_password,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "role": user_data.role,
                "department": user_data.department,
                "manager_id": user_data.manager_id,
                "phone": user_data.phone,
                "job_title": user_data.job_title,
                "location": user_data.location,
                "hire_date": user_data.hire_date,
                "salary": user_data.salary,
                "is_legendary": user_data.is_legendary,
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        db.commit()
        
        logger.info(f"➕ User created: {user_data.username} by {current_username}")
        
        # Return created user
        return await get_user_by_id(new_user_id, current_user, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error creating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

@router.put("/{user_id}", response_model=UserResponse, summary="✏️ Update User")
async def update_user(
    user_id: str = Path(..., description="User ID"),
    update_data: UserUpdateRequest = ...,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Update user by ID (requires admin+ role or own profile)
    """
    try:
        current_username = current_user.get("username")
        current_role = current_user.get("role")
        current_user_id = current_user.get("user_id")
        
        # Check permissions
        if (str(current_user_id) != user_id and 
            current_role not in ["admin", "founder"] and 
            current_username != "rickroll187"):
            # Managers can update their direct reports
            if current_role == "manager":
                # Check if target user reports to current user
                reports_to = db.execute(
                    text("SELECT manager_id FROM users WHERE user_id = :user_id"),
                    {"user_id": user_id}
                ).fetchone()
                
                if not reports_to or str(reports_to[0]) != str(current_user_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient privileges to update this user"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges to update this user"
                )
        
        # Check if user exists
        user_exists = db.execute(
            text("SELECT username FROM users WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Build update fields
        update_fields = []
        update_params = {"user_id": user_id}
        
        for field, value in update_data.dict(exclude_unset=True).items():
            # Restrict legendary status changes to admin+ roles
            if field == "is_legendary" and current_role not in ["admin", "founder"] and current_username != "rickroll187":
                continue
            
            # Validate manager_id if being updated
            if field == "manager_id" and value:
                manager_exists = db.execute(
                    text("SELECT user_id FROM users WHERE user_id = :manager_id"),
                    {"manager_id": value}
                ).fetchone()
                
                if not manager_exists:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid manager_id"
                    )
            
            if value is not None:
                update_fields.append(f"{field} = :{field}")
                update_params[field] = value
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        # Add updated_at timestamp
        update_fields.append("updated_at = :updated_at")
        update_params["updated_at"] = datetime.now(timezone.utc)
        
        # Execute update
        update_query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE user_id = :user_id
        """
        
        db.execute(text(update_query), update_params)
        db.commit()
        
        logger.info(f"✏️ User updated: {user_exists[0]} by {current_username}")
        
        # Return updated user
        return await get_user_by_id(user_id, current_user, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error updating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

@router.delete("/{user_id}", summary="🗑️ Deactivate User")
async def deactivate_user(
    user_id: str = Path(..., description="User ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Deactivate user (soft delete) - requires admin+ role
    """
    try:
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Check permissions
        if current_role not in ["admin", "founder"] and current_username != "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to deactivate users"
            )
        
        # Check if user exists and get username
        user_result = db.execute(
            text("SELECT username FROM users WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        
        if not user_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        target_username = user_result[0]
        
        # Prevent deactivating RICKROLL187
        if target_username == "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot deactivate the legendary founder RICKROLL187!"
            )
        
        # Deactivate user (soft delete)
        db.execute(
            text("""
                UPDATE users 
                SET is_active = false, 
                    deactivated_at = :deactivated_at,
                    deactivated_by = :deactivated_by
                WHERE user_id = :user_id
            """),
            {
                "user_id": user_id,
                "deactivated_at": datetime.now(timezone.utc),
                "deactivated_by": current_user.get("user_id")
            }
        )
        
        db.commit()
        
        logger.info(f"🗑️ User deactivated: {target_username} by {current_username}")
        
        return {
            "message": f"User {target_username} has been deactivated",
            "user_id": user_id,
            "deactivated_at": datetime.now(timezone.utc).isoformat(),
            "deactivated_by": current_username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error deactivating user: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate user"
        )

# =====================================
# 📊 USER STATISTICS ENDPOINTS 📊
# =====================================

@router.get("/stats/overview", response_model=UserStatsResponse, summary="📊 User Statistics")
async def get_user_statistics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get user statistics overview (requires manager+ role)
    """
    try:
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Check permissions
        if current_role not in ["manager", "hr_manager", "admin", "founder"] and current_username != "rickroll187":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to view user statistics"
            )
        
        # Get basic user counts
        user_counts = db.execute(
            text("""
                SELECT 
                    COUNT(*) as total_users,
                    SUM(CASE WHEN is_active THEN 1 ELSE 0 END) as active_users,
                    SUM(CASE WHEN is_legendary THEN 1 ELSE 0 END) as legendary_users,
                    SUM(CASE WHEN created_at >= NOW() - INTERVAL '30 days' THEN 1 ELSE 0 END) as recent_registrations
                FROM users
            """)
        ).fetchone()
        
        # Get department statistics
        dept_stats = db.execute(
            text("""
                SELECT department, COUNT(*) as count
                FROM users 
                WHERE is_active = true AND department IS NOT NULL
                GROUP BY department
                ORDER BY count DESC
            """)
        ).fetchall()
        
        # Get role statistics
        role_stats = db.execute(
            text("""
                SELECT role, COUNT(*) as count
                FROM users 
                WHERE is_active = true
                GROUP BY role
                ORDER BY count DESC
            """)
        ).fetchall()
        
        # Get legendary statistics
        legendary_stats_result = db.execute(
            text("""
                SELECT 
                    AVG(COALESCE(lm.swiss_precision_score, 0)) as avg_swiss_precision,
                    AVG(COALESCE(lm.code_bro_rating, 5)) as avg_code_bro_energy,
                    COUNT(la.user_id) as users_with_achievements,
                    SUM(la.achievement_count) as total_achievements
                FROM users u
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                LEFT JOIN (
                    SELECT user_id, COUNT(*) as achievement_count 
                    FROM legendary_achievements 
                    GROUP BY user_id
                ) la ON u.user_id = la.user_id
                WHERE u.is_legendary = true AND u.is_active = true
            """)
        ).fetchone()
        
        # Build response
        user_counts_dict = dict(user_counts._mapping)
        
        departments = {row[0]: row[1] for row in dept_stats}
        roles = {row[0]: row[1] for row in role_stats}
        
        legendary_stats = {
            "avg_swiss_precision_score": float(legendary_stats_result[0] or 0),
            "avg_code_bro_energy": float(legendary_stats_result[1] or 5),
            "users_with_achievements": int(legendary_stats_result[2] or 0),
            "total_achievements": int(legendary_stats_result[3] or 0),
            "rickroll187_status": "active" if current_username == "rickroll187" else "founder_active"
        }
        
        response = UserStatsResponse(
            total_users=user_counts_dict["total_users"],
            active_users=user_counts_dict["active_users"],
            legendary_users=user_counts_dict["legendary_users"],
            departments=departments,
            roles=roles,
            recent_registrations=user_counts_dict["recent_registrations"],
            legendary_stats=legendary_stats
        )
        
        logger.info(f"📊 User statistics retrieved by: {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting user statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user statistics"
        )

# =====================================
# 🎸 LEGENDARY USER MANAGEMENT 🎸
# =====================================

@router.post("/legendary/grant", summary="🎸 Grant Legendary Status")
async def grant_legendary_status(
    request_data: LegendaryUserRequest,
    current_user: Dict[str, Any] = Depends(verify_rickroll187),
    db: Session = Depends(get_db_session)
):
    """
    Grant or revoke legendary status (RICKROLL187 exclusive)
    """
    try:
        # Get target user
        target_user = db.execute(
            text("SELECT username, is_legendary FROM users WHERE user_id = :user_id"),
            {"user_id": request_data.user_id}
        ).fetchone()
        
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        target_username = target_user[0]
        current_legendary_status = target_user[1]
        
        # Update legendary status
        db.execute(
            text("""
                UPDATE users 
                SET is_legendary = :is_legendary,
                    updated_at = :updated_at
                WHERE user_id = :user_id
            """),
            {
                "user_id": request_data.user_id,
                "is_legendary": request_data.grant_legendary,
                "updated_at": datetime.now(timezone.utc)
            }
        )
        
        # Create or update legendary metrics if granting status
        if request_data.grant_legendary:
            db.execute(
                text("""
                    INSERT INTO legendary_metrics (
                        user_id, swiss_precision_score, code_bro_rating, 
                        swiss_precision_level, code_bro_energy_level, created_at
                    ) VALUES (
                        :user_id, 95.0, 9, :swiss_precision_level, :code_bro_energy_level, :created_at
                    ) ON CONFLICT (user_id) DO UPDATE SET
                        swiss_precision_level = :swiss_precision_level,
                        code_bro_energy_level = :code_bro_energy_level,
                        updated_at = :created_at
                """),
                {
                    "user_id": request_data.user_id,
                    "swiss_precision_level": request_data.swiss_precision_level,
                    "code_bro_energy_level": request_data.code_bro_energy_level,
                    "created_at": datetime.now(timezone.utc)
                }
            )
            
            # Award legendary status achievement
            db.execute(
                text("""
                    INSERT INTO legendary_achievements (
                        achievement_id, user_id, achievement_type, achievement_data, earned_at
                    ) VALUES (
                        :achievement_id, :user_id, 'legendary_status_granted', :achievement_data, :earned_at
                    )
                """),
                {
                    "achievement_id": str(uuid.uuid4()),
                    "user_id": request_data.user_id,
                    "achievement_data": {
                        "granted_by": "rickroll187",
                        "reason": request_data.reason,
                        "swiss_precision_level": request_data.swiss_precision_level,
                        "code_bro_energy_level": request_data.code_bro_energy_level
                    },
                    "earned_at": datetime.now(timezone.utc)
                }
            )
        
        db.commit()
        
        action = "granted" if request_data.grant_legendary else "revoked"
        logger.info(f"🎸 Legendary status {action} for {target_username} by RICKROLL187")
        
        return {
            "message": f"🎸 Legendary status {action} for {target_username}! 🎸",
            "user_id": request_data.user_id,
            "username": target_username,
            "previous_status": current_legendary_status,
            "new_status": request_data.grant_legendary,
            "reason": request_data.reason,
            "granted_by": "rickroll187",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "swiss_precision_level": request_data.swiss_precision_level if request_data.grant_legendary else None,
            "code_bro_energy_level": request_data.code_bro_energy_level if request_data.grant_legendary else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error managing legendary status: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to manage legendary status"
        )

@router.get("/legendary/candidates", summary="🎸 Legendary Candidates")
async def get_legendary_candidates(
    current_user: Dict[str, Any] = Depends(get_legendary_user),
    db: Session = Depends(get_db_session)
):
    """
    Get users who might be candidates for legendary status
    """
    try:
        # Get high-performing users who aren't already legendary
        candidates = db.execute(
            text("""
                SELECT u.user_id, u.username, u.first_name, u.last_name, u.role, u.department,
                       AVG(pr.overall_score) as avg_performance,
                       COUNT(pr.review_id) as review_count,
                       COALESCE(lm.swiss_precision_score, 0) as swiss_precision_score,
                       COALESCE(lm.code_bro_rating, 5) as code_bro_rating,
                       u.created_at
                FROM users u
                LEFT JOIN performance_reviews_enhanced pr ON u.user_id = pr.user_id
                LEFT JOIN legendary_metrics lm ON u.user_id = lm.user_id
                WHERE u.is_active = true 
                  AND u.is_legendary = false
                  AND u.username != 'rickroll187'
                  AND u.created_at <= NOW() - INTERVAL '90 days'  -- At least 3 months tenure
                GROUP BY u.user_id, u.username, u.first_name, u.last_name, u.role, u.department,
                         lm.swiss_precision_score, lm.code_bro_rating, u.created_at
                HAVING AVG(pr.overall_score) >= 4.0 OR COUNT(pr.review_id) = 0  -- High performers or new users
                ORDER BY AVG(pr.overall_score) DESC NULLS LAST, u.created_at
                LIMIT 20
            """)
        ).fetchall()
        
        candidate_list = []
        for candidate in candidates:
            candidate_dict = dict(candidate._mapping)
            candidate_list.append({
                "user_id": str(candidate_dict["user_id"]),
                "username": candidate_dict["username"],
                "full_name": f"{candidate_dict['first_name']} {candidate_dict['last_name']}",
                "role": candidate_dict["role"],
                "department": candidate_dict.get("department"),
                "avg_performance": float(candidate_dict["avg_performance"] or 0),
                "review_count": int(candidate_dict["review_count"] or 0),
                "swiss_precision_score": float(candidate_dict["swiss_precision_score"] or 0),
                "code_bro_rating": int(candidate_dict["code_bro_rating"] or 5),
                "tenure_days": (datetime.now(timezone.utc) - candidate_dict["created_at"]).days,
                "candidacy_score": float(candidate_dict["avg_performance"] or 0) * 20 + 
                                 float(candidate_dict["swiss_precision_score"] or 0) * 0.8 +
                                 int(candidate_dict["code_bro_rating"] or 5) * 5
            })
        
        # Sort by candidacy score
        candidate_list.sort(key=lambda x: x["candidacy_score"], reverse=True)
        
        logger.info(f"🎸 Legendary candidates retrieved by: {current_user.get('username')}")
        
        return {
            "candidates": candidate_list,
            "total_candidates": len(candidate_list),
            "evaluation_criteria": [
                "Average performance score >= 4.0",
                "Minimum 90 days tenure", 
                "Swiss precision score consideration",
                "Code bro energy rating",
                "Overall candidacy score calculation"
            ],
            "next_steps": [
                "Review candidate performance history",
                "Evaluate team collaboration impact", 
                "Consider Swiss precision contributions",
                "Submit to RICKROLL187 for approval"
            ]
        }
        
    except Exception as e:
        logger.error(f"🚨 Error getting legendary candidates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve legendary candidates"
        )

# =====================================
# 🎸 LEGENDARY EXPORTS 🎸
# =====================================

__all__ = ["router"]

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY USER MANAGEMENT SYSTEM LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"User management system loaded at: 2025-08-05 22:22:54 UTC")
    print("👤 Complete CRUD operations: ACTIVE")
    print("🎸 Legendary status management: RICKROLL187 EXCLUSIVE")
    print("📊 User statistics and analytics: ENABLED")
    print("⚡ Swiss precision user profiles: MAXIMUM")
    print("💪 Code bro energy integration: INFINITE")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
