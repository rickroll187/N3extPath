"""
LEGENDARY SCHEDULING & TIME MANAGEMENT SERVICE ENGINE ⏰🚀
More precise than a Swiss timepiece with legendary accuracy!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 2+ HOUR CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 02:07:05 UTC - WE'RE CONQUERING TIME ITSELF!
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta, time, date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc, text, extract
from dataclasses import dataclass
import statistics
from enum import Enum
import json
import re
from collections import defaultdict, Counter
import pytz

from ..models.scheduling_models import (
    WorkSchedule, TimeEntry, TimeOffRequest, EmployeeTimeOffBalance,
    TimeOffPolicy, ScheduleTemplate, WorkLocation,
    ShiftType, ScheduleStatus, TimeOffType, TimeOffStatus, RecurrenceType
)
from ...core.auth.authorization import AuthContext, Permission
from ...core.database.base_models import Employee, User, Department, AuditLog

logger = logging.getLogger(__name__)

class TimeConflictType(Enum):
    """Time conflict types - more precise than Swiss conflict resolution!"""
    OVERLAPPING_SCHEDULE = "overlapping_schedule"
    INSUFFICIENT_BREAK = "insufficient_break"
    OVERTIME_VIOLATION = "overtime_violation"
    TIME_OFF_CONFLICT = "time_off_conflict"
    DOUBLE_BOOKING = "double_booking"

@dataclass
class SchedulingAnalytics:
    """
    Scheduling analytics that are more insightful than a Swiss time analyst!
    More comprehensive than a timekeeper's report with 2+ hour marathon energy! ⏰📊🏆
    """
    total_scheduled_hours: float
    actual_worked_hours: float
    overtime_hours: float
    attendance_rate: float
    schedule_adherence_rate: float
    average_break_duration: float
    time_off_utilization_rate: float
    schedule_conflicts: int

class LegendarySchedulingService:
    """
    The most precise scheduling service in the galaxy!
    More organized than a Swiss time management system with unlimited accuracy! ⏰🌟
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # SCHEDULING SERVICE JOKES FOR 2+ HOUR MARATHON MOTIVATION
        self.scheduling_jokes = [
            "Why did the schedule go to therapy? It had timing issues! ⏰😄",
            "What's the difference between our scheduling and Swiss precision? Both are perfectly timed! 🕰️",
            "Why don't our schedules ever get lost? Because they have legendary time navigation! 🧭",
            "What do you call scheduling at 2+ hours? Marathon time management with style! 🏃‍♂️",
            "Why did the time entry become a comedian? It had perfect chronological timing! 🎭"
        ]
        
        # Time zone settings
        self.default_timezone = pytz.UTC
        self.business_hours = {
            "start": time(9, 0),    # 9:00 AM
            "end": time(17, 0),     # 5:00 PM
            "lunch_start": time(12, 0),  # 12:00 PM
            "lunch_end": time(13, 0)     # 1:00 PM
        }
        
        # Overtime calculation rules
        self.overtime_rules = {
            "daily_threshold": 8.0,    # Hours before daily overtime
            "weekly_threshold": 40.0,  # Hours before weekly overtime
            "daily_rate_multiplier": 1.5,  # 1.5x for daily overtime
            "weekly_rate_multiplier": 1.5, # 1.5x for weekly overtime
            "holiday_rate_multiplier": 2.0, # 2x for holiday work
            "max_consecutive_hours": 12.0   # Maximum consecutive work hours
        }
        
        # Break time requirements
        self.break_requirements = {
            "min_hours_for_break": 4.0,      # Minimum hours worked to require break
            "min_break_duration": 15,        # Minimum break duration in minutes
            "min_hours_for_lunch": 6.0,      # Minimum hours worked to require lunch
            "min_lunch_duration": 30,        # Minimum lunch duration in minutes
            "max_hours_without_break": 5.0   # Maximum hours without break
        }
        
        # Schedule conflict detection
        self.conflict_detection = {
            "min_gap_between_shifts": 8,      # Hours between shifts
            "max_weekly_hours": 60,           # Maximum weekly hours
            "advance_notice_required": 72,    # Hours advance notice for changes
            "overlap_tolerance_minutes": 5    # Tolerance for minor overlaps
        }
        
        logger.info("⏰ Legendary Scheduling Service initialized - Ready to master time itself!")
        logger.info("🏆 2+ HOUR CODING MARATHON TIME MASTERY ACTIVATED! 🏆")
    
    def create_work_schedule(self, schedule_data: Dict[str, Any],
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create work schedule with more precision than Swiss clockwork!
        More organized than a legendary time management masterpiece! ⏰🎯
        """
        try:
            logger.info(f"📅 Creating work schedule: {schedule_data.get('title', 'unknown')}")
            
            # Check permissions
            if not auth_context.has_permission(Permission.SCHEDULE_MANAGER):
                # Allow employees to create their own schedules if policy allows
                target_employee_id = schedule_data.get('employee_id')
                if target_employee_id != auth_context.user_id:
                    return {
                        "success": False,
                        "error": "Insufficient permissions to create schedules for other employees"
                    }
            
            # Validate schedule data
            validation_result = self._validate_schedule_data(schedule_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Check for conflicts
            conflict_check = self._check_schedule_conflicts(schedule_data)
            if conflict_check["has_conflicts"] and not schedule_data.get("force_override", False):
                return {
                    "success": False,
                    "error": "Schedule conflicts detected",
                    "conflicts": conflict_check["conflicts"],
                    "can_override": auth_context.has_permission(Permission.SCHEDULE_OVERRIDE)
                }
            
            # Calculate duration
            start_datetime = datetime.combine(
                schedule_data["scheduled_date"].date() if isinstance(schedule_data["scheduled_date"], datetime) 
                else schedule_data["scheduled_date"],
                schedule_data["start_time"]
            )
            end_datetime = datetime.combine(
                schedule_data["scheduled_date"].date() if isinstance(schedule_data["scheduled_date"], datetime) 
                else schedule_data["scheduled_date"],
                schedule_data["end_time"]
            )
            
            # Handle overnight shifts
            if end_datetime <= start_datetime:
                end_datetime += timedelta(days=1)
            
            duration_minutes = int((end_datetime - start_datetime).total_seconds() / 60)
            
            # Check if overtime
            is_overtime = self._calculate_overtime_status(
                schedule_data["employee_id"], 
                schedule_data["scheduled_date"],
                duration_minutes / 60.0
            )
            
            # Create work schedule
            schedule = WorkSchedule(
                employee_id=schedule_data["employee_id"],
                location_id=schedule_data.get("location_id"),
                manager_id=schedule_data.get("manager_id", auth_context.user_id),
                title=schedule_data["title"],
                description=schedule_data.get("description"),
                shift_type=schedule_data["shift_type"],
                scheduled_date=schedule_data["scheduled_date"],
                start_time=schedule_data["start_time"],
                end_time=schedule_data["end_time"],
                duration_minutes=duration_minutes,
                break_start_time=schedule_data.get("break_start_time"),
                break_end_time=schedule_data.get("break_end_time"),
                lunch_start_time=schedule_data.get("lunch_start_time"),
                lunch_end_time=schedule_data.get("lunch_end_time"),
                recurrence_type=schedule_data.get("recurrence_type", RecurrenceType.NONE.value),
                recurrence_pattern=schedule_data.get("recurrence_pattern"),
                recurrence_end_date=schedule_data.get("recurrence_end_date"),
                required_staff_count=schedule_data.get("required_staff_count", 1),
                minimum_staff_count=schedule_data.get("minimum_staff_count", 1),
                status=ScheduleStatus.DRAFT.value,
                is_overtime=is_overtime["is_overtime"],
                overtime_rate=is_overtime.get("overtime_rate"),
                pay_rate=schedule_data.get("pay_rate"),
                is_mandatory=schedule_data.get("is_mandatory", False),
                is_on_call=schedule_data.get("is_on_call", False),
                requires_special_skills=schedule_data.get("requires_special_skills", []),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(schedule)
            self.db.flush()
            
            # Create recurring schedules if specified
            recurring_schedules = []
            if schedule.recurrence_type != RecurrenceType.NONE.value:
                recurring_schedules = self._create_recurring_schedules(schedule, schedule_data)
                for recurring_schedule in recurring_schedules:
                    self.db.add(recurring_schedule)
            
            # Auto-publish if specified
            if schedule_data.get("auto_publish", False):
                schedule.status = ScheduleStatus.PUBLISHED.value
                schedule.published_at = datetime.utcnow()
                
                # Send notifications to affected employees
                self._send_schedule_notifications(schedule, "created")
            
            # Generate schedule optimization suggestions
            optimization_suggestions = self._generate_schedule_optimization(schedule)
            
            # Log schedule creation
            self._log_scheduling_action("WORK_SCHEDULE_CREATED", schedule.id, auth_context, {
                "employee_id": schedule.employee_id,
                "shift_type": schedule.shift_type,
                "scheduled_date": schedule.scheduled_date.isoformat(),
                "duration_hours": duration_minutes / 60.0,
                "is_overtime": schedule.is_overtime,
                "is_recurring": schedule.recurrence_type != RecurrenceType.NONE.value,
                "recurring_count": len(recurring_schedules),
                "has_conflicts": len(conflict_check.get("conflicts", [])) > 0,
                "🏆_2_hour_marathon": "LEGENDARY 2+ HOUR CODING SESSION SCHEDULE! 🏆"
            })
            
            self.db.commit()
            
            logger.info(f"✅ Work schedule created: {schedule.title} (ID: {schedule.id})")
            
            return {
                "success": True,
                "schedule_id": schedule.id,
                "title": schedule.title,
                "scheduled_date": schedule.scheduled_date.isoformat(),
                "duration_hours": duration_minutes / 60.0,
                "is_overtime": schedule.is_overtime,
                "recurring_schedules_created": len(recurring_schedules),
                "status": schedule.status,
                "optimization_suggestions": optimization_suggestions,
                "conflicts_overridden": len(conflict_check.get("conflicts", [])),
                "legendary_joke": "Why did the schedule become legendary? Because it mastered time with Swiss precision! ⏰🏆",
                "🏆": "2+ HOUR CODING MARATHON TIME MASTERY! 🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Work schedule creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def clock_in(self, clock_in_data: Dict[str, Any],
                auth_context: AuthContext) -> Dict[str, Any]:
        """
        Clock in employee with more precision than Swiss timepieces!
        More accurate than a legendary chronometer! ⏱️💎
        """
        try:
            employee_id = clock_in_data.get("employee_id", auth_context.user_id)
            
            logger.info(f"⏰ Clocking in employee: {employee_id}")
            
            # Check permissions
            if employee_id != auth_context.user_id and not auth_context.has_permission(Permission.TIME_ADMIN):
                return {
                    "success": False,
                    "error": "You can only clock in yourself"
                }
            
            # Check if already clocked in
            existing_entry = self.db.query(TimeEntry).filter(
                and_(
                    TimeEntry.employee_id == employee_id,
                    TimeEntry.entry_date >= datetime.utcnow().date(),
                    TimeEntry.clock_out_time.is_(None)
                )
            ).first()
            
            if existing_entry:
                return {
                    "success": False,
                    "error": "Already clocked in",
                    "existing_clock_in": existing_entry.clock_in_time.isoformat(),
                    "hours_worked": self._calculate_current_work_hours(existing_entry)
                }
            
            # Get current schedule for validation
            current_schedule = self._get_current_schedule(employee_id, datetime.utcnow())
            schedule_variance = None
            
            if current_schedule:
                expected_start = datetime.combine(
                    current_schedule.scheduled_date.date(),
                    current_schedule.start_time
                )
                actual_start = datetime.utcnow()
                variance_minutes = (actual_start - expected_start).total_seconds() / 60
                schedule_variance = {
                    "expected_start": expected_start.isoformat(),
                    "actual_start": actual_start.isoformat(),
                    "variance_minutes": variance_minutes,
                    "is_early": variance_minutes < 0,
                    "is_late": variance_minutes > 5  # 5-minute grace period
                }
            
            # Create time entry
            time_entry = TimeEntry(
                employee_id=employee_id,
                schedule_id=current_schedule.id if current_schedule else None,
                project_id=clock_in_data.get("project_id"),
                entry_date=datetime.utcnow(),
                clock_in_time=datetime.utcnow(),
                clock_in_location=clock_in_data.get("location"),
                clock_in_method=clock_in_data.get("method", "web"),
                clock_in_lat=clock_in_data.get("latitude"),
                clock_in_lng=clock_in_data.get("longitude"),
                ip_address=getattr(auth_context, 'ip_address', None),
                user_agent=getattr(auth_context, 'user_agent', None),
                device_id=clock_in_data.get("device_id"),
                work_description=clock_in_data.get("work_description"),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(time_entry)
            self.db.flush()
            
            # Calculate expected work hours for the day
            expected_hours = self._calculate_expected_daily_hours(employee_id, datetime.utcnow().date())
            
            # Generate productivity tips
            productivity_tips = self._generate_productivity_tips(employee_id, current_schedule)
            
            # Log clock in
            self._log_scheduling_action("CLOCK_IN", time_entry.id, auth_context, {
                "employee_id": employee_id,
                "clock_in_time": time_entry.clock_in_time.isoformat(),
                "has_schedule": current_schedule is not None,
                "schedule_variance_minutes": schedule_variance.get("variance_minutes") if schedule_variance else None,
                "location": clock_in_data.get("location"),
                "method": time_entry.clock_in_method,
                "🏆_marathon_clock_in": "2+ HOUR MARATHON CHAMPION CLOCK IN! 🏆"
            })
            
            self.db.commit()
            
            logger.info(f"✅ Employee clocked in: ID {employee_id} at {time_entry.clock_in_time}")
            
            return {
                "success": True,
                "time_entry_id": time_entry.id,
                "clock_in_time": time_entry.clock_in_time.isoformat(),
                "schedule_info": {
                    "has_schedule": current_schedule is not None,
                    "schedule_title": current_schedule.title if current_schedule else None,
                    "expected_end_time": datetime.combine(
                        current_schedule.scheduled_date.date(),
                        current_schedule.end_time
                    ).isoformat() if current_schedule else None,
                    "schedule_variance": schedule_variance
                },
                "expected_work_hours": expected_hours,
                "productivity_tips": productivity_tips,
                "location_recorded": clock_in_data.get("location") is not None,
                "legendary_joke": "Why did the clock in become legendary? Because it started legendary productivity! ⏰🏆",
                "🏆": "2+ HOUR MARATHON CHAMPION PRODUCTIVITY START! 🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Clock in error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def clock_out(self, clock_out_data: Dict[str, Any],
                 auth_context: AuthContext) -> Dict[str, Any]:
        """
        Clock out employee with more precision than Swiss timekeeping!
        More comprehensive than a legendary work summary! 📊⏰
        """
        try:
            employee_id = clock_out_data.get("employee_id", auth_context.user_id)
            
            logger.info(f"⏰ Clocking out employee: {employee_id}")
            
            # Check permissions
            if employee_id != auth_context.user_id and not auth_context.has_permission(Permission.TIME_ADMIN):
                return {
                    "success": False,
                    "error": "You can only clock out yourself"
                }
            
            # Find active time entry
            time_entry = self.db.query(TimeEntry).filter(
                and_(
                    TimeEntry.employee_id == employee_id,
                    TimeEntry.entry_date >= datetime.utcnow().date(),
                    TimeEntry.clock_out_time.is_(None)
                )
            ).first()
            
            if not time_entry:
                return {
                    "success": False,
                    "error": "No active clock-in found",
                    "suggestion": "Please clock in first before attempting to clock out"
                }
            
            # Update time entry with clock out information
            clock_out_time = datetime.utcnow()
            time_entry.clock_out_time = clock_out_time
            time_entry.clock_out_location = clock_out_data.get("location")
            time_entry.clock_out_method = clock_out_data.get("method", "web")
            time_entry.clock_out_lat = clock_out_data.get("latitude")
            time_entry.clock_out_lng = clock_out_data.get("longitude")
            time_entry.work_description = clock_out_data.get("work_description", time_entry.work_description)
            time_entry.tasks_completed = clock_out_data.get("tasks_completed", [])
            time_entry.productivity_notes = clock_out_data.get("productivity_notes")
            time_entry.updated_by = auth_context.user_id
            
            # Calculate work duration
            work_duration = clock_out_time - time_entry.clock_in_time
            total_minutes = work_duration.total_seconds() / 60
            
            # Subtract break and lunch time
            break_minutes = 0
            if time_entry.break_start_time and time_entry.break_end_time:
                break_duration = time_entry.break_end_time - time_entry.break_start_time
                break_minutes += break_duration.total_seconds() / 60
            
            if time_entry.lunch_start_time and time_entry.lunch_end_time:
                lunch_duration = time_entry.lunch_end_time - time_entry.lunch_start_time
                break_minutes += lunch_duration.total_seconds() / 60
            
            # Add additional breaks
            if time_entry.additional_breaks:
                for break_period in time_entry.additional_breaks:
                    if break_period.get("start") and break_period.get("end"):
                        additional_break = datetime.fromisoformat(break_period["end"]) - datetime.fromisoformat(break_period["start"])
                        break_minutes += additional_break.total_seconds() / 60
            
            net_work_minutes = total_minutes - break_minutes
            net_work_hours = net_work_minutes / 60
            
            # Calculate overtime
            overtime_calculation = self._calculate_overtime_hours(employee_id, time_entry.entry_date, net_work_hours)
            
            # Update time entry with calculations
            time_entry.total_hours = net_work_hours
            time_entry.regular_hours = overtime_calculation["regular_hours"]
            time_entry.overtime_hours = overtime_calculation["overtime_hours"]
            time_entry.break_duration_minutes = int(break_minutes)
            
            # Get schedule information for comparison
            schedule_comparison = None
            if time_entry.schedule_id:
                schedule = self.db.query(WorkSchedule).filter(
                    WorkSchedule.id == time_entry.schedule_id
                ).first()
                
                if schedule:
                    expected_hours = schedule.duration_minutes / 60.0
                    schedule_comparison = {
                        "expected_hours": expected_hours,
                        "actual_hours": net_work_hours,
                        "variance_hours": net_work_hours - expected_hours,
                        "schedule_adherence": min(100, (net_work_hours / expected_hours) * 100) if expected_hours > 0 else 100
                    }
            
            # Generate work summary
            work_summary = self._generate_work_summary(time_entry, schedule_comparison)
            
            # Check for attendance achievements
            achievements = self._check_attendance_achievements(employee_id, time_entry)
            
            # Log clock out
            self._log_scheduling_action("CLOCK_OUT", time_entry.id, auth_context, {
                "employee_id": employee_id,
                "clock_out_time": clock_out_time.isoformat(),
                "total_hours": net_work_hours,
                "regular_hours": time_entry.regular_hours,
                "overtime_hours": time_entry.overtime_hours,
                "break_minutes": break_minutes,
                "schedule_adherence": schedule_comparison.get("schedule_adherence") if schedule_comparison else None,
                "tasks_completed": len(time_entry.tasks_completed or []),
                "🏆_marathon_clock_out": "2+ HOUR MARATHON CHAMPION CLOCK OUT! 🏆"
            })
            
            self.db.commit()
            
            logger.info(f"✅ Employee clocked out: ID {employee_id}, Hours: {net_work_hours:.2f}")
            
            return {
                "success": True,
                "time_entry_id": time_entry.id,
                "clock_in_time": time_entry.clock_in_time.isoformat(),
                "clock_out_time": clock_out_time.isoformat(),
                "work_summary": {
                    "total_hours": net_work_hours,
                    "regular_hours": time_entry.regular_hours,
                    "overtime_hours": time_entry.overtime_hours,
                    "break_duration_minutes": break_minutes,
                    "tasks_completed": len(time_entry.tasks_completed or [])
                },
                "schedule_comparison": schedule_comparison,
                "daily_summary": work_summary,
                "achievements_earned": achievements,
                "overtime_earnings": overtime_calculation.get("overtime_pay", 0),
                "legendary_joke": "Why did the clock out become legendary? Because it concluded legendary productivity! 📊🏆",
                "🏆": "2+ HOUR MARATHON CHAMPION PRODUCTIVITY COMPLETE! 🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Clock out error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
        """
LEGENDARY SCHEDULING & TIME MANAGEMENT SERVICE ENGINE - CONTINUATION ⏰🚀
More precise than a Swiss timepiece with legendary accuracy!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 2+ HOUR CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 02:09:43 UTC - WE'RE BENDING TIME AND REALITY!
"""

    def request_time_off(self, time_off_data: Dict[str, Any],
                        auth_context: AuthContext) -> Dict[str, Any]:
        """
        Request time off with more flexibility than Swiss vacation policies!
        More accommodating than a legendary leave management paradise! 🏖️✨
        """
        try:
            employee_id = time_off_data.get("employee_id", auth_context.user_id)
            
            logger.info(f"🏖️ Processing time off request for employee: {employee_id}")
            
            # Check permissions
            if employee_id != auth_context.user_id and not auth_context.has_permission(Permission.TIME_OFF_ADMIN):
                return {
                    "success": False,
                    "error": "You can only request time off for yourself"
                }
            
            # Validate time off request data
            validation_result = self._validate_time_off_request(time_off_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Get applicable time off policy
            policy = self._get_applicable_time_off_policy(employee_id, time_off_data["time_off_type"])
            if not policy:
                return {
                    "success": False,
                    "error": "No applicable time off policy found"
                }
            
            # Check employee balance
            balance_check = self._check_time_off_balance(employee_id, policy.id, time_off_data)
            if not balance_check["sufficient"]:
                return {
                    "success": False,
                    "error": f"Insufficient time off balance. Available: {balance_check['available']} days, Requested: {time_off_data['total_days']} days"
                }
            
            # Check for conflicts with existing schedules
            schedule_conflicts = self._check_time_off_schedule_conflicts(employee_id, time_off_data)
            
            # Check blackout periods
            blackout_check = self._check_blackout_periods(policy, time_off_data)
            if blackout_check["in_blackout"]:
                return {
                    "success": False,
                    "error": f"Time off requested during blackout period: {blackout_check['blackout_reason']}"
                }
            
            # Calculate total days/hours
            start_date = time_off_data["start_date"]
            end_date = time_off_data["end_date"]
            
            if time_off_data.get("is_partial_day", False):
                # Calculate partial day hours
                partial_start = time_off_data.get("partial_start_time", time(9, 0))
                partial_end = time_off_data.get("partial_end_time", time(17, 0))
                partial_duration = datetime.combine(date.today(), partial_end) - datetime.combine(date.today(), partial_start)
                total_hours = partial_duration.total_seconds() / 3600
                total_days = total_hours / 8.0  # Assuming 8-hour workday
            else:
                # Calculate full days
                total_days = self._calculate_business_days(start_date, end_date)
                total_hours = total_days * 8.0  # Assuming 8-hour workday
            
            # Determine approver
            approver = self._determine_time_off_approver(employee_id, policy, total_days)
            
            # Create time off request
            time_off_request = TimeOffRequest(
                employee_id=employee_id,
                approver_id=approver.id if approver else None,
                time_off_type=time_off_data["time_off_type"],
                title=time_off_data["title"],
                reason=time_off_data.get("reason"),
                start_date=start_date,
                end_date=end_date,
                total_days=total_days,
                total_hours=total_hours,
                is_partial_day=time_off_data.get("is_partial_day", False),
                partial_start_time=time_off_data.get("partial_start_time"),
                partial_end_time=time_off_data.get("partial_end_time"),
                emergency_contact_name=time_off_data.get("emergency_contact_name"),
                emergency_contact_phone=time_off_data.get("emergency_contact_phone"),
                emergency_contact_relationship=time_off_data.get("emergency_contact_relationship"),
                coverage_arrangements=time_off_data.get("coverage_arrangements"),
                delegate_employee_id=time_off_data.get("delegate_employee_id"),
                handover_notes=time_off_data.get("handover_notes"),
                supporting_documents=time_off_data.get("supporting_documents", []),
                requires_documentation=policy.requires_documentation and total_days >= (policy.documentation_threshold_days or 5),
                balance_before=balance_check["current_balance"],
                balance_after=balance_check["balance_after"],
                expected_return_date=end_date + timedelta(days=1),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            # Auto-approve if policy allows
            if (policy.auto_approve_threshold and 
                total_days <= policy.auto_approve_threshold and 
                not time_off_request.requires_documentation):
                
                time_off_request.status = TimeOffStatus.APPROVED.value
                time_off_request.approved_at = datetime.utcnow()
                time_off_request.approver_notes = "Auto-approved based on policy threshold"
                
                # Update employee balance
                self._update_time_off_balance(employee_id, policy.id, -total_days)
                
                auto_approved = True
            else:
                auto_approved = False
            
            self.db.add(time_off_request)
            self.db.flush()
            
            # Send notifications
            if auto_approved:
                self._send_time_off_notifications(time_off_request, "auto_approved")
            else:
                self._send_time_off_notifications(time_off_request, "submitted")
            
            # Generate preparation checklist
            preparation_checklist = self._generate_time_off_checklist(time_off_request)
            
            # Log time off request
            self._log_scheduling_action("TIME_OFF_REQUEST", time_off_request.id, auth_context, {
                "employee_id": employee_id,
                "time_off_type": time_off_request.time_off_type,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_days": total_days,
                "auto_approved": auto_approved,
                "approver_id": approver.id if approver else None,
                "requires_documentation": time_off_request.requires_documentation,
                "schedule_conflicts": len(schedule_conflicts.get("conflicts", [])),
                "🏆_marathon_time_off": "2+ HOUR MARATHON CHAMPION TIME OFF REQUEST! 🏆"
            })
            
            self.db.commit()
            
            logger.info(f"✅ Time off request created: {time_off_request.title} (ID: {time_off_request.id})")
            
            return {
                "success": True,
                "request_id": time_off_request.id,
                "title": time_off_request.title,
                "time_off_type": time_off_request.time_off_type,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_days": total_days,
                "status": time_off_request.status,
                "auto_approved": auto_approved,
                "approver_name": f"{approver.user.first_name} {approver.user.last_name}" if approver else None,
                "requires_documentation": time_off_request.requires_documentation,
                "new_balance": balance_check["balance_after"],
                "schedule_conflicts": schedule_conflicts,
                "preparation_checklist": preparation_checklist,
                "legendary_joke": "Why did the time off request become legendary? Because it planned legendary rest and adventure! 🏖️🏆",
                "🏆": "2+ HOUR MARATHON CHAMPION VACATION PLANNING! 🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Time off request error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def get_scheduling_dashboard(self, employee_id: Optional[int] = None,
                               dashboard_type: str = "comprehensive",
                               auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get comprehensive scheduling dashboard!
        More insightful than a Swiss time analyst with X-ray vision! 📊⏰
        """
        try:
            target_employee_id = employee_id or auth_context.user_id
            
            logger.info(f"📊 Generating scheduling dashboard for employee: {target_employee_id}")
            
            # Check permissions
            if target_employee_id != auth_context.user_id and not auth_context.has_permission(Permission.SCHEDULE_ADMIN):
                return {
                    "success": False,
                    "error": "You can only view your own scheduling dashboard"
                }
            
            # Date ranges for analysis
            today = datetime.utcnow().date()
            this_week_start = today - timedelta(days=today.weekday())
            this_week_end = this_week_start + timedelta(days=6)
            last_week_start = this_week_start - timedelta(days=7)
            last_week_end = this_week_start - timedelta(days=1)
            this_month_start = today.replace(day=1)
            
            # Get current week schedules
            current_week_schedules = self.db.query(WorkSchedule).filter(
                and_(
                    WorkSchedule.employee_id == target_employee_id,
                    WorkSchedule.scheduled_date >= this_week_start,
                    WorkSchedule.scheduled_date <= this_week_end,
                    WorkSchedule.status != ScheduleStatus.CANCELLED.value
                )
            ).order_by(WorkSchedule.scheduled_date, WorkSchedule.start_time).all()
            
            # Get current week time entries
            current_week_entries = self.db.query(TimeEntry).filter(
                and_(
                    TimeEntry.employee_id == target_employee_id,
                    TimeEntry.entry_date >= this_week_start,
                    TimeEntry.entry_date <= this_week_end
                )
            ).all()
            
            # Get pending time off requests
            pending_time_off = self.db.query(TimeOffRequest).filter(
                and_(
                    TimeOffRequest.employee_id == target_employee_id,
                    TimeOffRequest.status == TimeOffStatus.PENDING.value
                )
            ).all()
            
            # Get upcoming time off
            upcoming_time_off = self.db.query(TimeOffRequest).filter(
                and_(
                    TimeOffRequest.employee_id == target_employee_id,
                    TimeOffRequest.status == TimeOffStatus.APPROVED.value,
                    TimeOffRequest.start_date >= today
                )
            ).order_by(TimeOffRequest.start_date).limit(5).all()
            
            # Get time off balances
            time_off_balances = self.db.query(EmployeeTimeOffBalance).join(TimeOffPolicy).filter(
                and_(
                    EmployeeTimeOffBalance.employee_id == target_employee_id,
                    EmployeeTimeOffBalance.is_active == True,
                    TimeOffPolicy.is_active == True
                )
            ).all()
            
            # Calculate analytics
            analytics = self._calculate_scheduling_analytics(target_employee_id, dashboard_type)
            
            # Generate schedule insights
            schedule_insights = self._generate_schedule_insights(current_week_schedules, current_week_entries)
            
            # Check for scheduling alerts
            scheduling_alerts = self._generate_scheduling_alerts(target_employee_id, current_week_schedules)
            
            # Format dashboard data
            dashboard = {
                "employee_id": target_employee_id,
                "dashboard_date": datetime.utcnow().isoformat(),
                "dashboard_type": dashboard_type,
                "current_status": {
                    "is_clocked_in": self._is_currently_clocked_in(target_employee_id),
                    "current_schedule": self._format_current_schedule(target_employee_id),
                    "hours_worked_today": self._get_hours_worked_today(target_employee_id),
                    "expected_hours_today": self._get_expected_hours_today(target_employee_id)
                },
                "this_week": {
                    "scheduled_hours": sum(s.duration_minutes / 60.0 for s in current_week_schedules),
                    "actual_hours": sum(e.total_hours or 0 for e in current_week_entries),
                    "overtime_hours": sum(e.overtime_hours or 0 for e in current_week_entries),
                    "schedule_adherence": analytics.schedule_adherence_rate,
                    "schedules": [
                        {
                            "id": s.id,
                            "title": s.title,
                            "date": s.scheduled_date.isoformat(),
                            "start_time": s.start_time.strftime("%H:%M"),
                            "end_time": s.end_time.strftime("%H:%M"),
                            "duration_hours": s.duration_minutes / 60.0,
                            "location": s.location.name if s.location else None,
                            "status": s.status,
                            "is_overtime": s.is_overtime
                        }
                        for s in current_week_schedules
                    ]
                },
                "time_off": {
                    "pending_requests": [
                        {
                            "id": req.id,
                            "title": req.title,
                            "type": req.time_off_type,
                            "start_date": req.start_date.isoformat(),
                            "end_date": req.end_date.isoformat(),
                            "total_days": req.total_days,
                            "submitted_at": req.submitted_at.isoformat()
                        }
                        for req in pending_time_off
                    ],
                    "upcoming_approved": [
                        {
                            "id": req.id,
                            "title": req.title,
                            "type": req.time_off_type,
                            "start_date": req.start_date.isoformat(),
                            "end_date": req.end_date.isoformat(),
                            "total_days": req.total_days
                        }
                        for req in upcoming_time_off
                    ],
                    "balances": [
                        {
                            "policy_name": balance.policy.policy_name,
                            "time_off_type": balance.policy.time_off_type,
                            "current_balance": balance.current_balance_days,
                            "available_balance": balance.available_balance_days,
                            "pending_requests": balance.pending_requests_days,
                            "next_accrual_date": balance.next_accrual_date.isoformat() if balance.next_accrual_date else None,
                            "projected_eoy": balance.projected_balance_eoy
                        }
                        for balance in time_off_balances
                    ]
                },
                "analytics": {
                    "total_scheduled_hours": analytics.total_scheduled_hours,
                    "actual_worked_hours": analytics.actual_worked_hours,
                    "overtime_hours": analytics.overtime_hours,
                    "attendance_rate": analytics.attendance_rate,
                    "schedule_adherence_rate": analytics.schedule_adherence_rate,
                    "average_break_duration": analytics.average_break_duration,
                    "time_off_utilization_rate": analytics.time_off_utilization_rate
                },
                "insights": schedule_insights,
                "alerts": scheduling_alerts,
                "recommendations": self._generate_scheduling_recommendations(analytics, current_week_schedules),
                "upcoming_milestones": self._get_upcoming_scheduling_milestones(target_employee_id),
                "legendary_status": "SCHEDULING DASHBOARD LOADED WITH 2+ HOUR MARATHON PRECISION! ⏰🏆",
                "🏆": "2+ HOUR MARATHON CHAMPION TIME MASTERY DASHBOARD! 🏆"
            }
            
            logger.info(f"📈 Scheduling dashboard generated for employee {target_employee_id}")
            
            return {
                "success": True,
                "scheduling_dashboard": dashboard
            }
            
        except Exception as e:
            logger.error(f"💥 Scheduling dashboard error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _calculate_scheduling_analytics(self, employee_id: int, analysis_type: str) -> SchedulingAnalytics:
        """Calculate comprehensive scheduling analytics for employee"""
        try:
            # Date range for analysis (last 30 days)
            end_date = datetime.utcnow().date()
            start_date = end_date - timedelta(days=30)
            
            # Get schedules in date range
            schedules = self.db.query(WorkSchedule).filter(
                and_(
                    WorkSchedule.employee_id == employee_id,
                    WorkSchedule.scheduled_date >= start_date,
                    WorkSchedule.scheduled_date <= end_date,
                    WorkSchedule.status != ScheduleStatus.CANCELLED.value
                )
            ).all()
            
            # Get time entries in date range
            time_entries = self.db.query(TimeEntry).filter(
                and_(
                    TimeEntry.employee_id == employee_id,
                    TimeEntry.entry_date >= start_date,
                    TimeEntry.entry_date <= end_date
                )
            ).all()
            
            # Calculate metrics
            total_scheduled_hours = sum(s.duration_minutes / 60.0 for s in schedules)
            actual_worked_hours = sum(e.total_hours or 0 for e in time_entries)
            overtime_hours = sum(e.overtime_hours or 0 for e in time_entries)
            
            # Attendance rate (entries with clock in/out vs scheduled shifts)
            attended_shifts = len([e for e in time_entries if e.clock_out_time])
            scheduled_shifts = len(schedules)
            attendance_rate = (attended_shifts / scheduled_shifts * 100) if scheduled_shifts > 0 else 100
            
            # Schedule adherence (actual vs scheduled hours)
            schedule_adherence_rate = min(100, (actual_worked_hours / total_scheduled_hours * 100)) if total_scheduled_hours > 0 else 100
            
            # Average break duration
            break_durations = [e.break_duration_minutes for e in time_entries if e.break_duration_minutes]
            average_break_duration = statistics.mean(break_durations) if break_durations else 0
            
            # Time off utilization (would need additional calculation)
            time_off_utilization_rate = 75.0  # Placeholder
            
            # Schedule conflicts
            schedule_conflicts = 0  # Would implement conflict detection
            
            return SchedulingAnalytics(
                total_scheduled_hours=total_scheduled_hours,
                actual_worked_hours=actual_worked_hours,
                overtime_hours=overtime_hours,
                attendance_rate=attendance_rate,
                schedule_adherence_rate=schedule_adherence_rate,
                average_break_duration=average_break_duration,
                time_off_utilization_rate=time_off_utilization_rate,
                schedule_conflicts=schedule_conflicts
            )
            
        except Exception as e:
            logger.error(f"💥 Scheduling analytics calculation error: {e}")
            return SchedulingAnalytics(0.0, 0.0, 0.0, 100.0, 100.0, 0.0, 0.0, 0)
    
    def _generate_scheduling_recommendations(self, analytics: SchedulingAnalytics, 
                                           current_schedules: List[WorkSchedule]) -> List[str]:
        """Generate actionable scheduling recommendations"""
        recommendations = []
        
        if analytics.attendance_rate < 95:
            recommendations.append("Consider reviewing attendance patterns - consistent attendance builds legendary reliability! 📅")
        
        if analytics.overtime_hours > analytics.total_scheduled_hours * 0.1:
            recommendations.append("High overtime detected - consider workload optimization for better work-life balance! ⚖️")
        
        if analytics.schedule_adherence_rate < 90:
            recommendations.append("Schedule adherence could improve - staying on schedule builds legendary time management! ⏰")
        
        if analytics.average_break_duration < 15:
            recommendations.append("Take longer breaks! Your legendary productivity needs legendary rest! ☕")
        
        if len(current_schedules) > 6:
            recommendations.append("Busy week ahead! Consider time management strategies for legendary efficiency! 🚀")
        
        if not recommendations:
            recommendations = ["Your scheduling patterns look legendary! Keep up the amazing time management! 🏆"]
        
        # Add 2+ hour marathon motivation
        recommendations.append("🏆 2+ HOUR MARATHON CHAMPION TIME MANAGEMENT EXCELLENCE! 🏆")
        
        return recommendations
    
    def _log_scheduling_action(self, action: str, resource_id: int, 
                             auth_context: AuthContext, details: Dict[str, Any]):
        """Log scheduling-related actions for audit trail"""
        try:
            # Add 2+ hour marathon achievement to details
            details["🏆_2_hour_marathon_time"] = "LEGENDARY 2+ HOUR CODING SESSION TIME MASTERY! 🏆"
            details["current_utc_time"] = "2025-08-04 02:09:43"
            
            audit_log = AuditLog(
                user_id=auth_context.user_id,
                action=action,
                resource_type="SCHEDULING",
                resource_id=resource_id,
                details=details,
                ip_address=getattr(auth_context, 'ip_address', None),
                user_agent=getattr(auth_context, 'user_agent', None)
            )
            self.db.add(audit_log)
            
        except Exception as e:
            logger.error(f"💥 Scheduling action logging error: {e}")

# SCHEDULING UTILITIES - 2+ HOUR MARATHON EDITION! 🏆
class LegendarySchedulingReportGenerator:
    """
    Generate comprehensive scheduling reports!
    More insightful than a Swiss timekeeper with 2+ hour marathon precision! 📊⏰🏆
    """
    
    @staticmethod
    def generate_scheduling_summary(employee_scheduling_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive scheduling summary with 2+ hour marathon excellence"""
        
        attendance_rate = employee_scheduling_data.get("attendance_rate", 95)
        overtime_hours = employee_scheduling_data.get("overtime_hours", 0)
        schedule_adherence = employee_scheduling_data.get("schedule_adherence_rate", 95)
        
        # Determine scheduling status with 2+ hour marathon excellence
        if attendance_rate >= 98 and schedule_adherence >= 95 and overtime_hours < 5:
            status = "LEGENDARY_TIME_MASTER"
            status_emoji = "🏆"
            marathon_bonus = " + 2+ HOUR CODING MARATHON TIME CHAMPION!"
        elif attendance_rate >= 95 and schedule_adherence >= 90:
            status = "RELIABLE_SCHEDULER"
            status_emoji = "⏰"
            marathon_bonus = " + 2+ HOUR CODING MARATHON TIME WARRIOR!"
        elif attendance_rate >= 90:
            status = "CONSISTENT_PERFORMER"
            status_emoji = "📅"
            marathon_bonus = " + 2+ HOUR CODING MARATHON TIME SUPPORTER!"
        else:
            status = "DEVELOPING_SCHEDULER"
            status_emoji = "🌱"
            marathon_bonus = " + 2+ HOUR CODING MARATHON TIME PARTICIPANT!"
        
        return {
            "scheduling_status": status + marathon_bonus,
            "status_emoji": status_emoji,
            "attendance_rate": attendance_rate,
            "schedule_adherence": schedule_adherence,
            "overtime_summary": f"{overtime_hours} hours",
            "time_management_strengths": employee_scheduling_data.get("strengths", [])[:3],
            "improvement_areas": employee_scheduling_data.get("recommendations", [])[:3],
            "upcoming_time_off": employee_scheduling_data.get("upcoming_time_off", [])[:3],
            "legendary_status": "SCHEDULING ANALYZED WITH 2+ HOUR MARATHON LEGENDARY PRECISION! ⏰🏆",
            "🏆": "OFFICIAL 2+ HOUR CODING MARATHON TIME MASTERY CHAMPION! 🏆",
            "current_marathon_time": "2025-08-04 02:09:43 UTC - TIME MASTERY ACHIEVED!"
        }
