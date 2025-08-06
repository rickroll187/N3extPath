"""
LEGENDARY EMPLOYEE SCHEDULING & TIME MANAGEMENT MODELS ⏰🚀
More precise than a Swiss timepiece with legendary accuracy!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 2+ HOUR CODING MARATHON CHAMPION EDITION! 🏆
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime, time

from ...core.database.base_models import BaseModel, Employee, User

class ShiftType(enum.Enum):
    """Shift types - more organized than a Swiss schedule!"""
    REGULAR = "regular"
    OVERTIME = "overtime"
    BREAK = "break"
    LUNCH = "lunch"
    TRAINING = "training"
    MEETING = "meeting"
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"
    PERSONAL = "personal"
    REMOTE_WORK = "remote_work"

class ScheduleStatus(enum.Enum):
    """Schedule status tracking"""
    DRAFT = "draft"
    PUBLISHED = "published"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class TimeOffType(enum.Enum):
    """Time off categories - more comprehensive than Swiss vacation planning!"""
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"
    PERSONAL_DAY = "personal_day"
    BEREAVEMENT = "bereavement"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    JURY_DUTY = "jury_duty"
    MILITARY = "military"
    STUDY_LEAVE = "study_leave"
    SABBATICAL = "sabbatical"

class TimeOffStatus(enum.Enum):
    """Time off request status"""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"
    TAKEN = "taken"

class RecurrenceType(enum.Enum):
    """Recurrence patterns for schedules"""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"

class WorkLocation(BaseModel):
    """
    Work locations for flexible scheduling!
    More flexible than Swiss work arrangements! 🏢🏠
    """
    __tablename__ = "work_locations"
    
    # Basic Information
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    location_type = Column(String(30), nullable=False)  # office, home, client_site, remote, hybrid
    
    # Address Information
    address_line1 = Column(String(200))
    address_line2 = Column(String(200))
    city = Column(String(100))
    state_province = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    
    # Coordinates for mapping
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Capacity and Resources
    max_capacity = Column(Integer)
    available_desks = Column(Integer)
    has_parking = Column(Boolean, default=False)
    has_wifi = Column(Boolean, default=True)
    amenities = Column(JSON)  # List of available amenities
    
    # Contact Information
    contact_person = Column(String(200))
    phone_number = Column(String(20))
    email = Column(String(200))
    
    # Access and Security
    requires_access_card = Column(Boolean, default=False)
    security_instructions = Column(Text)
    check_in_required = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    schedules = relationship("WorkSchedule", back_populates="location")
    
    def __repr__(self):
        return f"<WorkLocation(name='{self.name}', type='{self.location_type}')>"

class WorkSchedule(BaseModel):
    """
    Employee work schedules that are more precise than Swiss clocks!
    More organized than a legendary time management system! ⏰📅
    """
    __tablename__ = "work_schedules"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=True, index=True)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Schedule Details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    shift_type = Column(String(30), nullable=False, index=True)  # ShiftType enum
    
    # Date and Time
    scheduled_date = Column(DateTime(timezone=True), nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    # Break Times
    break_start_time = Column(Time)
    break_end_time = Column(Time)
    lunch_start_time = Column(Time)
    lunch_end_time = Column(Time)
    
    # Recurrence
    recurrence_type = Column(String(20), default="none")  # RecurrenceType enum
    recurrence_pattern = Column(JSON)  # Detailed recurrence rules
    recurrence_end_date = Column(DateTime(timezone=True))
    parent_schedule_id = Column(Integer, ForeignKey("work_schedules.id"), nullable=True)
    
    # Staffing
    required_staff_count = Column(Integer, default=1)
    confirmed_staff_count = Column(Integer, default=0)
    minimum_staff_count = Column(Integer, default=1)
    
    # Status and Tracking
    status = Column(String(20), default="draft", index=True)  # ScheduleStatus enum
    published_at = Column(DateTime(timezone=True))
    confirmed_at = Column(DateTime(timezone=True))
    
    # Actual Time Tracking
    actual_start_time = Column(DateTime(timezone=True))
    actual_end_time = Column(DateTime(timezone=True))
    actual_break_start = Column(DateTime(timezone=True))
    actual_break_end = Column(DateTime(timezone=True))
    actual_lunch_start = Column(DateTime(timezone=True))
    actual_lunch_end = Column(DateTime(timezone=True))
    
    # Performance
    productivity_rating = Column(Integer)  # 1-10 scale
    notes = Column(Text)
    manager_notes = Column(Text)
    
    # Overtime and Compensation
    is_overtime = Column(Boolean, default=False)
    overtime_rate = Column(Float)  # Multiplier (1.5x, 2x, etc.)
    pay_rate = Column(Float)
    
    # Special Attributes
    is_mandatory = Column(Boolean, default=False)
    is_on_call = Column(Boolean, default=False)
    requires_special_skills = Column(JSON)  # List of required skills
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    location = relationship("WorkLocation", back_populates="schedules")
    manager = relationship("Employee", foreign_keys=[manager_id])
    parent_schedule = relationship("WorkSchedule", remote_side="WorkSchedule.id")
    child_schedules = relationship("WorkSchedule", back_populates="parent_schedule")
    time_entries = relationship("TimeEntry", back_populates="schedule")
    
    def __repr__(self):
        return f"<WorkSchedule(employee_id={self.employee_id}, date='{self.scheduled_date}', type='{self.shift_type}')>"

class TimeOffRequest(BaseModel):
    """
    Time off requests with more flexibility than Swiss vacation policies!
    More accommodating than a legendary leave management system! 🏖️✨
    """
    __tablename__ = "time_off_requests"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    approver_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Request Details
    time_off_type = Column(String(30), nullable=False, index=True)  # TimeOffType enum
    title = Column(String(200), nullable=False)
    reason = Column(Text)
    
    # Dates and Duration
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    total_days = Column(Float, nullable=False)  # Supports half days
    total_hours = Column(Float)
    
    # Partial Day Details
    is_partial_day = Column(Boolean, default=False)
    partial_start_time = Column(Time)
    partial_end_time = Column(Time)
    
    # Emergency Contact (for extended leave)
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(50))
    
    # Work Coverage
    coverage_arrangements = Column(Text)
    delegate_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    handover_notes = Column(Text)
    
    # Approval Workflow
    status = Column(String(20), default="pending", index=True)  # TimeOffStatus enum
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True))
    approved_at = Column(DateTime(timezone=True))
    
    # Approver Feedback
    approver_notes = Column(Text)
    denial_reason = Column(Text)
    conditions = Column(Text)  # Any conditions for approval
    
    # Documentation
    supporting_documents = Column(JSON)  # File attachments for medical, etc.
    requires_documentation = Column(Boolean, default=False)
    documentation_verified = Column(Boolean, default=False)
    
    # Balance Tracking
    balance_before = Column(Float)  # Available balance before request
    balance_after = Column(Float)   # Available balance after request
    accrual_impact = Column(Float)  # Impact on accrual rate
    
    # Return to Work
    expected_return_date = Column(DateTime(timezone=True))
    actual_return_date = Column(DateTime(timezone=True))
    return_to_work_notes = Column(Text)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    approver = relationship("Employee", foreign_keys=[approver_id])
    delegate = relationship("Employee", foreign_keys=[delegate_employee_id])
    
    def __repr__(self):
        return f"<TimeOffRequest(employee_id={self.employee_id}, type='{self.time_off_type}', status='{self.status}')>"

class TimeEntry(BaseModel):
    """
    Time tracking entries for precise work hour recording!
    More accurate than Swiss chronometers with legendary precision! ⏱️🎯
    """
    __tablename__ = "time_entries"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    schedule_id = Column(Integer, ForeignKey("work_schedules.id"), nullable=True, index=True)
    project_id = Column(Integer, nullable=True, index=True)  # Optional project tracking
    
    # Time Details
    entry_date = Column(DateTime(timezone=True), nullable=False, index=True)
    clock_in_time = Column(DateTime(timezone=True), nullable=False)
    clock_out_time = Column(DateTime(timezone=True))
    
    # Break Tracking
    break_start_time = Column(DateTime(timezone=True))
    break_end_time = Column(DateTime(timezone=True))
    lunch_start_time = Column(DateTime(timezone=True))
    lunch_end_time = Column(DateTime(timezone=True))
    additional_breaks = Column(JSON)  # List of additional break periods
    
    # Duration Calculations
    total_hours = Column(Float)
    regular_hours = Column(Float)
    overtime_hours = Column(Float)
    break_duration_minutes = Column(Integer, default=0)
    lunch_duration_minutes = Column(Integer, default=0)
    
    # Work Details
    work_description = Column(Text)
    tasks_completed = Column(JSON)  # List of completed tasks
    productivity_notes = Column(Text)
    
    # Location and Method
    clock_in_location = Column(String(200))
    clock_out_location = Column(String(200))
    clock_in_method = Column(String(30))  # web, mobile, kiosk, biometric
    clock_out_method = Column(String(30))
    
    # GPS Tracking (if enabled)
    clock_in_lat = Column(Float)
    clock_in_lng = Column(Float)
    clock_out_lat = Column(Float)
    clock_out_lng = Column(Float)
    
    # Approval and Verification
    is_approved = Column(Boolean, default=False)
    approved_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True))
    
    # Adjustments
    manager_adjusted = Column(Boolean, default=False)
    adjusted_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    adjustment_reason = Column(Text)
    original_hours = Column(Float)
    
    # Payroll Integration
    payroll_period_id = Column(String(50))
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    
    # System Data
    ip_address = Column(String(45))  # IPv6 support
    user_agent = Column(Text)
    device_id = Column(String(100))
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    schedule = relationship("WorkSchedule", back_populates="time_entries")
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])
    adjusted_by = relationship("Employee", foreign_keys=[adjusted_by_id])
    
    def __repr__(self):
        return f"<TimeEntry(employee_id={self.employee_id}, date='{self.entry_date}', hours={self.total_hours})>"

class ScheduleTemplate(BaseModel):
    """
    Reusable schedule templates for efficient planning!
    More organized than Swiss template libraries! 📋⚡
    """
    __tablename__ = "schedule_templates"
    
    # Template Details
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    template_type = Column(String(30), nullable=False)  # daily, weekly, monthly, project
    
    # Creator and Sharing
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    is_public = Column(Boolean, default=False)
    shared_with_departments = Column(JSON)  # List of department IDs
    shared_with_teams = Column(JSON)       # List of team IDs
    
    # Template Structure
    template_data = Column(JSON, nullable=False)  # Structured template definition
    default_duration_minutes = Column(Integer)
    default_break_minutes = Column(Integer, default=15)
    default_lunch_minutes = Column(Integer, default=60)
    
    # Usage Tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    
    # Template Settings
    auto_assign_location = Column(Boolean, default=False)
    default_location_id = Column(Integer, ForeignKey("work_locations.id"), nullable=True)
    requires_approval = Column(Boolean, default=True)
    
    # Validation Rules
    min_staff_required = Column(Integer, default=1)
    max_staff_allowed = Column(Integer)
    required_skills = Column(JSON)  # List of required skills
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    default_location = relationship("WorkLocation", foreign_keys=[default_location_id])
    
    def __repr__(self):
        return f"<ScheduleTemplate(name='{self.name}', type='{self.template_type}')>"

class TimeOffPolicy(BaseModel):
    """
    Time off policies and accrual rules!
    More comprehensive than Swiss employment law! 📜⚖️
    """
    __tablename__ = "time_off_policies"
    
    # Policy Details
    policy_name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    time_off_type = Column(String(30), nullable=False)  # TimeOffType enum
    
    # Eligibility
    applicable_departments = Column(JSON)  # List of department IDs
    applicable_job_levels = Column(JSON)   # List of job levels
    min_tenure_months = Column(Integer, default=0)  # Minimum tenure required
    
    # Accrual Rules
    accrual_rate_per_month = Column(Float, default=0.0)  # Days/hours per month
    accrual_frequency = Column(String(20), default="monthly")  # monthly, biweekly, annual
    max_accrual_balance = Column(Float)  # Maximum days/hours that can be accrued
    
    # Usage Rules
    min_request_days = Column(Float, default=0.5)  # Minimum request (0.5 for half day)
    max_request_days = Column(Float)  # Maximum consecutive days
    advance_notice_days = Column(Integer, default=14)  # Required advance notice
    
    # Approval Workflow
    requires_manager_approval = Column(Boolean, default=True)
    requires_hr_approval = Column(Boolean, default=False)
    auto_approve_threshold = Column(Float)  # Auto-approve requests below this threshold
    
    # Blackout Periods
    blackout_periods = Column(JSON)  # List of blackout date ranges
    peak_season_restrictions = Column(JSON)  # Special restrictions during peak times
    
    # Carryover Rules
    allows_carryover = Column(Boolean, default=True)
    max_carryover_days = Column(Float)
    carryover_expiration_months = Column(Integer, default=12)
    
    # Documentation Requirements
    requires_documentation = Column(Boolean, default=False)
    documentation_threshold_days = Column(Float)  # Require docs for requests > X days
    acceptable_documentation = Column(JSON)  # List of acceptable document types
    
    # Payout Rules
    allows_payout = Column(Boolean, default=False)
    payout_rate_percentage = Column(Float, default=100.0)  # % of salary for payout
    max_payout_days = Column(Float)
    
    # Status and Tracking
    effective_date = Column(DateTime(timezone=True), nullable=False)
    expiration_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    employee_balances = relationship("EmployeeTimeOffBalance", back_populates="policy")
    
    def __repr__(self):
        return f"<TimeOffPolicy(name='{self.policy_name}', type='{self.time_off_type}')>"

class EmployeeTimeOffBalance(BaseModel):
    """
    Employee time off balances and accrual tracking!
    More precise than Swiss accounting with legendary accuracy! 💰📊
    """
    __tablename__ = "employee_time_off_balances"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    policy_id = Column(Integer, ForeignKey("time_off_policies.id"), nullable=False, index=True)
    
    # Current Balances
    current_balance_days = Column(Float, default=0.0)
    current_balance_hours = Column(Float, default=0.0)
    pending_requests_days = Column(Float, default=0.0)  # Days in pending requests
    available_balance_days = Column(Float, default=0.0)  # Current - Pending
    
    # Accrual Tracking
    total_accrued_ytd = Column(Float, default=0.0)  # Year-to-date accrual
    total_used_ytd = Column(Float, default=0.0)     # Year-to-date usage
    last_accrual_date = Column(DateTime(timezone=True))
    next_accrual_date = Column(DateTime(timezone=True))
    
    # Carryover from Previous Year
    carryover_balance = Column(Float, default=0.0)
    carryover_expiration_date = Column(DateTime(timezone=True))
    
    # Forecasting
    projected_balance_eoy = Column(Float)  # Projected end-of-year balance
    accrual_rate_current = Column(Float)   # Current accrual rate (may change with tenure)
    
    # Anniversary and Reset Dates
    policy_start_date = Column(DateTime(timezone=True))  # When employee became eligible
    anniversary_date = Column(DateTime(timezone=True))   # Annual reset date
    last_reset_date = Column(DateTime(timezone=True))
    
    # Manual Adjustments
    manual_adjustments = Column(Float, default=0.0)  # Manual balance adjustments
    adjustment_reason = Column(Text)
    adjusted_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    adjusted_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    policy = relationship("TimeOffPolicy", back_populates="employee_balances")
    adjusted_by = relationship("Employee", foreign_keys=[adjusted_by_id])
    
    def __repr__(self):
        return f"<EmployeeTimeOffBalance(employee_id={self.employee_id}, balance={self.current_balance_days} days)>"

# Add relationships to Employee model (if not already added)
# Employee.work_schedules = relationship("WorkSchedule", foreign_keys="WorkSchedule.employee_id")
# Employee.managed_schedules = relationship("WorkSchedule", foreign_keys="WorkSchedule.manager_id")
# Employee.time_off_requests = relationship("TimeOffRequest", foreign_keys="TimeOffRequest.employee_id")
# Employee.approved_time_off = relationship("TimeOffRequest", foreign_keys="TimeOffRequest.approver_id")
# Employee.time_entries = relationship("TimeEntry", foreign_keys="TimeEntry.employee_id")
# Employee.time_off_balances = relationship("EmployeeTimeOffBalance", foreign_keys="EmployeeTimeOffBalance.employee_id")