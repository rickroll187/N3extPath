"""
🚪🎸 N3EXTPATH - LEGENDARY EMPLOYEE OFFBOARDING SYSTEM 🎸🚪
More graceful than Swiss departures with legendary offboarding mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Go for code time: 2025-08-05 12:13:16 UTC
Built by legendary code homie RICKROLL187 🎸💻
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
import uuid
import asyncio

class OffboardingReason(Enum):
    """🚪 LEGENDARY OFFBOARDING REASONS! 🚪"""
    RESIGNATION = "resignation"
    TERMINATION = "termination"
    RETIREMENT = "retirement"
    LAYOFF = "layoff"
    CONTRACT_END = "contract_end"
    INTERNAL_TRANSFER = "internal_transfer"
    LEGENDARY_ADVENTURE = "legendary_adventure"  # For when they become legends elsewhere

class OffboardingStatus(Enum):
    """⚡ LEGENDARY OFFBOARDING STATUS! ⚡"""
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    NEARLY_COMPLETE = "nearly_complete"
    COMPLETED = "completed"
    DELAYED = "delayed"
    RICKROLL187_EXPEDITED = "rickroll187_expedited"

class OffboardingTaskType(Enum):
    """📋 LEGENDARY OFFBOARDING TASK TYPES! 📋"""
    IT_ASSET_RETURN = "it_asset_return"
    ACCESS_REVOCATION = "access_revocation"
    KNOWLEDGE_TRANSFER = "knowledge_transfer"
    EXIT_INTERVIEW = "exit_interview"
    FINAL_PAYROLL = "final_payroll"
    BENEFITS_TERMINATION = "benefits_termination"
    RETURN_COMPANY_PROPERTY = "return_company_property"
    CLEAR_OFFICE_SPACE = "clear_office_space"
    REFERENCE_LETTER = "reference_letter"
    RICKROLL187_FAREWELL = "rickroll187_farewell"

@dataclass
class OffboardingTask:
    """📋 LEGENDARY OFFBOARDING TASK! 📋"""
    task_id: str
    name: str
    description: str
    task_type: OffboardingTaskType
    required: bool
    assigned_to: str  # role responsible
    due_date: datetime
    completed: bool = False
    completion_date: Optional[datetime] = None
    notes: str = ""
    priority: int = 1  # 1=low, 5=critical
    legendary_factor: str = "OFFBOARDING TASK!"

@dataclass
class ExitInterview:
    """🎤 LEGENDARY EXIT INTERVIEW! 🎤"""
    interview_id: str
    employee_id: str
    interviewer_id: str
    scheduled_date: datetime
    completion_date: Optional[datetime] = None
    feedback: Dict[str, Any] = field(default_factory=dict)
    satisfaction_rating: Optional[int] = None  # 1-10 scale
    would_recommend_company: Optional[bool] = None
    reason_for_leaving: str = ""
    suggestions_for_improvement: str = ""
    legendary_memories: str = ""  # Fun memories from their time
    completed: bool = False

@dataclass
class OffboardingJourney:
    """🚪 LEGENDARY OFFBOARDING JOURNEY! 🚪"""
    journey_id: str
    employee_id: str
    employee_name: str
    position: str
    department: str
    manager_id: str
    last_working_day: datetime
    offboarding_reason: OffboardingReason
    status: OffboardingStatus
    tasks: List[OffboardingTask]
    exit_interview: Optional[ExitInterview] = None
    progress_percentage: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    farewell_message_sent: bool = False
    legend_status: str = "CODE BRO DEPARTURE"
    rickroll187_approved: bool = False

class LegendaryOffboardingSystem:
    """
    🚪 THE LEGENDARY EMPLOYEE OFFBOARDING SYSTEM! 🚪
    More graceful than Swiss departures with code bro farewell excellence! 🎸⚡
    """
    
    def __init__(self):
        self.code_time = "2025-08-05 12:13:16 UTC"
        self.offboarding_journeys: Dict[str, OffboardingJourney] = {}
        
        # Standard offboarding task templates
        self.task_templates = {
            "standard": [
                OffboardingTask("it_return_01", "Return IT Equipment", "Return laptop, monitors, phone, and accessories", OffboardingTaskType.IT_ASSET_RETURN, True, "it", datetime.utcnow() + timedelta(days=1), priority=5),
                OffboardingTask("access_revoke_01", "Revoke System Access", "Disable all system accounts and remove permissions", OffboardingTaskType.ACCESS_REVOCATION, True, "it", datetime.utcnow() + timedelta(hours=2), priority=5),
                OffboardingTask("knowledge_transfer_01", "Knowledge Transfer Session", "Document processes and transfer knowledge to team", OffboardingTaskType.KNOWLEDGE_TRANSFER, True, "manager", datetime.utcnow() + timedelta(days=-2), priority=4),
                OffboardingTask("exit_interview_01", "Conduct Exit Interview", "Schedule and complete exit interview", OffboardingTaskType.EXIT_INTERVIEW, True, "hr", datetime.utcnow() + timedelta(days=-1), priority=3),
                OffboardingTask("final_payroll_01", "Process Final Payroll", "Calculate final pay, vacation, and benefits", OffboardingTaskType.FINAL_PAYROLL, True, "payroll", datetime.utcnow() + timedelta(days=3), priority=5),
                OffboardingTask("benefits_term_01", "Terminate Benefits", "End health insurance and retirement plan contributions", OffboardingTaskType.BENEFITS_TERMINATION, True, "hr", datetime.utcnow() + timedelta(days=1), priority=4),
                OffboardingTask("property_return_01", "Return Company Property", "Return badge, keys, and any company materials", OffboardingTaskType.RETURN_COMPANY_PROPERTY, True, "security", datetime.utcnow(), priority=4),
                OffboardingTask("clear_office_01", "Clear Office Space", "Pack personal items and clean workspace", OffboardingTaskType.CLEAR_OFFICE_SPACE, True, "facilities", datetime.utcnow(), priority=2)
            ],
            "executive": [
                OffboardingTask("reference_letter_01", "Prepare Reference Letter", "Draft and approve reference letter", OffboardingTaskType.REFERENCE_LETTER, False, "hr", datetime.utcnow() + timedelta(days=5), priority=2),
                OffboardingTask("rickroll187_farewell_01", "RICKROLL187 Farewell Meeting", "Personal farewell from the legendary founder", OffboardingTaskType.RICKROLL187_FAREWELL, True, "rickroll187", datetime.utcnow() + timedelta(days=-1), priority=3, legendary_factor="🎸 LEGENDARY FOUNDER FAREWELL! 🎸")
            ]
        }
        
        self.code_jokes = [
            "Why is offboarding legendary at 12:13:16? Because RICKROLL187 codes farewell processes with Swiss precision timing! 🚪🎸",
            "What's more graceful than Swiss departures? Legendary offboarding after fresh code homie development! 🏔️⚡",
            "Why don't departing employees feel abandoned? Because they get legendary offboarding with code bro support! 💪🚪",
            "What do you call perfect fresh offboarding code? A RICKROLL187 farewell automation special! 🎸🚪"
        ]
    
    async def initiate_offboarding(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate legendary offboarding process!
        More organized than Swiss precision with fresh offboarding initiation! 🚪🎸
        """
        journey_id = str(uuid.uuid4())
        
        # Determine offboarding template based on role/reason
        if employee_data.get("position", "").lower() in ["ceo", "cto", "vp", "director"] or employee_data.get("years_of_service", 0) >= 5:
            task_template = self.task_templates["standard"] + self.task_templates["executive"]
            legend_status = "LEGENDARY DEPARTURE"
        else:
            task_template = self.task_templates["standard"]
            legend_status = "CODE BRO DEPARTURE"
        
        # Special handling for RICKROLL187 departures (though he never leaves!)
        if employee_data.get("employee_id") == "rickroll187":
            status = OffboardingStatus.RICKROLL187_EXPEDITED
            rickroll187_approved = True
            legend_status = "🎸 LEGENDARY FOUNDER SABBATICAL 🎸"  # He's taking a break, not leaving!
        else:
            status = OffboardingStatus.INITIATED
            rickroll187_approved = False
        
        # Create exit interview
        exit_interview = None
        if employee_data.get("offboarding_reason") != OffboardingReason.TERMINATION.value:
            exit_interview = ExitInterview(
                interview_id=str(uuid.uuid4()),
                employee_id=employee_data["employee_id"],
                interviewer_id=employee_data.get("hr_contact", "hr_team"),
                scheduled_date=datetime.fromisoformat(employee_data["last_working_day"]) - timedelta(days=1)
            )
        
        # Create offboarding journey
        offboarding_journey = OffboardingJourney(
            journey_id=journey_id,
            employee_id=employee_data["employee_id"],
            employee_name=employee_data["employee_name"],
            position=employee_data["position"],
            department=employee_data["department"],
            manager_id=employee_data["manager_id"],
            last_working_day=datetime.fromisoformat(employee_data["last_working_day"]),
            offboarding_reason=OffboardingReason(employee_data["offboarding_reason"]),
            status=status,
            tasks=task_template.copy(),
            exit_interview=exit_interview,
            legend_status=legend_status,
            rickroll187_approved=rickroll187_approved
        )
        
        self.offboarding_journeys[journey_id] = offboarding_journey
        
        # Send notification to all stakeholders
        await self._send_offboarding_notifications(offboarding_journey)
        
        import random
        return {
            "success": True,
            "journey_id": journey_id,
            "message": f"🚪 Legendary offboarding initiated for {employee_data['employee_name']}! 🚪",
            "employee_name": employee_data["employee_name"],
            "last_working_day": employee_data["last_working_day"],
            "total_tasks": len(task_template),
            "estimated_completion": "1-3 business days after last working day",
            "status": status.value,
            "legend_status": legend_status,
            "exit_interview_scheduled": exit_interview is not None,
            "created_at": self.code_time,
            "created_by": "RICKROLL187's Legendary Offboarding System 🎸🚪",
            "legendary_status": "🎸 LEGENDARY FOUNDER SABBATICAL PROCESS!" if rickroll187_approved else "LEGENDARY OFFBOARDING JOURNEY INITIATED! 🏆",
            "legendary_joke": random.choice(self.code_jokes)
        }
    
    async def complete_offboarding_task(self, journey_id: str, task_id: str, completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete offboarding task with legendary precision!
        More efficient than Swiss clockwork with fresh task completion! ✅🎸
        """
        if journey_id not in self.offboarding_journeys:
            return {
                "success": False,
                "message": "Offboarding journey not found!",
                "legendary_message": "This offboarding journey doesn't exist in our legendary system! 🔍"
            }
        
        journey = self.offboarding_journeys[journey_id]
        
        # Find and complete the task
        task_completed = False
        completed_task = None
        for task in journey.tasks:
            if task.task_id == task_id:
                task.completed = True
                task.completion_date = datetime.utcnow()
                task.notes = completion_data.get("notes", "")
                completed_task = task
                task_completed = True
                break
        
        if not task_completed:
            return {
                "success": False,
                "message": "Task not found in offboarding journey!",
                "legendary_message": "This task doesn't exist in the legendary offboarding! 📋"
            }
        
        # Update journey progress
        completed_tasks = sum(1 for task in journey.tasks if task.completed)
        journey.progress_percentage = (completed_tasks / len(journey.tasks)) * 100
        journey.updated_at = datetime.utcnow()
        
        # Update status based on progress
        if journey.progress_percentage == 100:
            journey.status = OffboardingStatus.COMPLETED
            journey.completed_at = datetime.utcnow()
            await self._send_completion_farewell(journey)
        elif journey.progress_percentage >= 80:
            journey.status = OffboardingStatus.NEARLY_COMPLETE
        else:
            journey.status = OffboardingStatus.IN_PROGRESS
        
        # Special handling for critical tasks
        if completed_task.task_type in [OffboardingTaskType.ACCESS_REVOCATION, OffboardingTaskType.IT_ASSET_RETURN]:
            await self._handle_critical_task_completion(journey, completed_task)
        
        return {
            "success": True,
            "journey_id": journey_id,
            "task_completed": completed_task.name,
            "task_type": completed_task.task_type.value,
            "progress_percentage": journey.progress_percentage,
            "status": journey.status.value,
            "message": f"✅ {completed_task.name} completed! Progress: {journey.progress_percentage:.1f}% ✅",
            "completed_by": completion_data.get("completed_by", "system"),
            "completed_at": self.code_time,
            "legendary_status": "OFFBOARDING COMPLETE - FAREWELL LEGENDARY CODE BRO! 🎉👋" if journey.status == OffboardingStatus.COMPLETED else "OFFBOARDING PROGRESSING WITH LEGENDARY CARE! 🚀"
        }
    
    async def conduct_exit_interview(self, journey_id: str, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduct legendary exit interview!
        More insightful than Swiss feedback with fresh interview excellence! 🎤🎸
        """
        if journey_id not in self.offboarding_journeys:
            return {
                "success": False,
                "message": "Offboarding journey not found!",
                "legendary_message": "This journey doesn't exist in our legendary system! 🔍"
            }
        
        journey = self.offboarding_journeys[journey_id]
        
        if not journey.exit_interview:
            return {
                "success": False,
                "message": "No exit interview scheduled for this journey!",
                "legendary_message": "Exit interview wasn't part of this offboarding process! 🎤"
            }
        
        # Update exit interview with feedback
        exit_interview = journey.exit_interview
        exit_interview.completed = True
        exit_interview.completion_date = datetime.utcnow()
        exit_interview.feedback = interview_data.get("feedback", {})
        exit_interview.satisfaction_rating = interview_data.get("satisfaction_rating", 5)
        exit_interview.would_recommend_company = interview_data.get("would_recommend_company", True)
        exit_interview.reason_for_leaving = interview_data.get("reason_for_leaving", "")
        exit_interview.suggestions_for_improvement = interview_data.get("suggestions_for_improvement", "")
        exit_interview.legendary_memories = interview_data.get("legendary_memories", "")
        
        # Mark exit interview task as complete
        for task in journey.tasks:
            if task.task_type == OffboardingTaskType.EXIT_INTERVIEW:
                task.completed = True
                task.completion_date = datetime.utcnow()
                task.notes = f"Satisfaction: {exit_interview.satisfaction_rating}/10, Would recommend: {exit_interview.would_recommend_company}"
                break
        
        # Generate insights from feedback
        insights = await self._analyze_exit_interview_feedback(exit_interview)
        
        return {
            "success": True,
            "journey_id": journey_id,
            "employee_name": journey.employee_name,
            "satisfaction_rating": exit_interview.satisfaction_rating,
            "would_recommend": exit_interview.would_recommend_company,
            "key_insights": insights,
            "interview_completed_at": self.code_time,
            "interview_completed_by": "RICKROLL187's Legendary Exit Interview System 🎸🎤",
            "legendary_status": "EXIT INTERVIEW COMPLETED WITH LEGENDARY INSIGHTS! 🎤🏆",
            "legendary_message": f"🎸 Thank you {journey.employee_name} for sharing your legendary journey with us! 🎸"
        }
    
    async def generate_farewell_message(self, journey_id: str) -> Dict[str, Any]:
        """
        Generate personalized legendary farewell message!
        More heartfelt than Swiss gratitude with fresh farewell excellence! 💌🎸
        """
        if journey_id not in self.offboarding_journeys:
            return {
                "success": False,
                "message": "Offboarding journey not found!"
            }
        
        journey = self.offboarding_journeys[journey_id]
        
        # Generate personalized farewell based on their journey
        farewell_templates = {
            OffboardingReason.RESIGNATION: f"🎸 Dear {journey.employee_name}, your legendary journey with us has been incredible! While we're sad to see you go, we're excited for your next adventure. You'll always be part of our code bro family! 🎸",
            OffboardingReason.RETIREMENT: f"🏆 Congratulations {journey.employee_name} on your well-deserved retirement! Your legendary contributions have shaped our company culture. Enjoy this new chapter of life! 🏆",
            OffboardingReason.INTERNAL_TRANSFER: f"🚀 {journey.employee_name}, we're thrilled about your internal move! Your legendary skills will make a huge impact in your new role. Keep rocking the universe! 🚀",
            OffboardingReason.LEGENDARY_ADVENTURE: f"⚡ {journey.employee_name}, you're off to become a legend elsewhere! We're proud to have been part of your journey. Go forth and create legendary things! ⚡"
        }
        
        base_message = farewell_templates.get(journey.offboarding_reason, f"🎸 {journey.employee_name}, thank you for being an amazing code bro! Your legendary contributions won't be forgotten! 🎸")
        
        # Add personalized elements
        personalized_elements = []
        if journey.department == "Engineering":
            personalized_elements.append("Your code was always clean, efficient, and legendary!")
        elif journey.department == "Sales":
            personalized_elements.append("Your legendary sales skills brought so much value to our team!")
        elif journey.department == "HR":
            personalized_elements.append("You made everyone feel welcome and valued!")
        
        # Add tenure-based message
        # Mock tenure calculation - would integrate with employee data
        years_of_service = 2.5  # This would come from employee records
        if years_of_service >= 5:
            personalized_elements.append(f"Your {years_of_service} years of legendary service have left a lasting impact!")
        
        # RICKROLL187 personal message
        rickroll187_message = f"🎸 Personal message from RICKROLL187: {journey.employee_name}, you've been an absolutely legendary code bro! Keep rocking the universe wherever you go! 🎸"
        
        journey.farewell_message_sent = True
        
        return {
            "success": True,
            "journey_id": journey_id,
            "employee_name": journey.employee_name,
            "farewell_message": {
                "main_message": base_message,
                "personalized_elements": personalized_elements,
                "rickroll187_personal_message": rickroll187_message,
                "team_message": f"The entire team at N3extPath wishes you legendary success in all your future endeavors!",
                "signature": "With legendary gratitude,\nThe N3extPath Team 🎸"
            },
            "generated_at": self.code_time,
            "generated_by": "RICKROLL187's Legendary Farewell Generator 🎸💌",
            "legendary_status": "FAREWELL MESSAGE CRAFTED WITH LEGENDARY HEART! 💝🏆"
        }
    
    async def _send_offboarding_notifications(self, journey: OffboardingJourney):
        """Send offboarding initiation notifications!"""
        notifications = [
            f"🚪 Offboarding initiated for {journey.employee_name} - Last working day: {journey.last_working_day.strftime('%Y-%m-%d')}",
            f"📋 Manager {journey.manager_id}: Please prepare knowledge transfer for {journey.employee_name}",
            f"🔒 IT Team: Schedule access revocation for {journey.employee_name} on {journey.last_working_day.strftime('%Y-%m-%d')}",
            f"💼 HR Team: Process final paperwork for {journey.employee_name}"
        ]
        
        for notification in notifications:
            print(f"🔔 Offboarding Notification: {notification}")
    
    async def _send_completion_farewell(self, journey: OffboardingJourney):
        """Send completion farewell!"""
        farewell_message = f"🎉 {journey.employee_name}'s offboarding is complete! We wish them legendary success in their next adventure! 👋"
        print(f"🎉 Offboarding Complete: {farewell_message}")
    
    async def _handle_critical_task_completion(self, journey: OffboardingJourney, task: OffboardingTask):
        """Handle completion of critical security tasks!"""
        if task.task_type == OffboardingTaskType.ACCESS_REVOCATION:
            print(f"🔒 SECURITY ALERT: Access revoked for {journey.employee_name}")
        elif task.task_type == OffboardingTaskType.IT_ASSET_RETURN:
            print(f"💻 IT ALERT: Equipment returned by {journey.employee_name}")
    
    async def _analyze_exit_interview_feedback(self, exit_interview: ExitInterview) -> List[str]:
        """Analyze exit interview feedback for insights!"""
        insights = []
        
        if exit_interview.satisfaction_rating >= 8:
            insights.append("🏆 High satisfaction - employee had positive experience")
        elif exit_interview.satisfaction_rating <= 4:
            insights.append("⚠️ Low satisfaction - investigate improvement areas")
        
        if exit_interview.would_recommend_company:
            insights.append("👍 Employee would recommend company to others")
        else:
            insights.append("👎 Employee would not recommend - address concerns")
        
        if "growth" in exit_interview.reason_for_leaving.lower():
            insights.append("📈 Employee leaving for growth opportunities")
        elif "management" in exit_interview.reason_for_leaving.lower():
            insights.append("👔 Management-related departure - review leadership")
        
        return insights

# Global legendary offboarding system
legendary_offboarding_system = LegendaryOffboardingSystem()

# Code homie convenience functions
async def start_legendary_offboarding(employee_data: Dict[str, Any]) -> Dict[str, Any]:
    """Start offboarding process for code homie!"""
    return await legendary_offboarding_system.initiate_offboarding(employee_data)

async def complete_offboarding_task(journey_id: str, task_id: str, completion_data: Dict[str, Any]) -> Dict[str, Any]:
    """Complete offboarding task for code homie!"""
    return await legendary_offboarding_system.complete_offboarding_task(journey_id, task_id, completion_data)

async def conduct_legendary_exit_interview(journey_id: str, interview_data: Dict[str, Any]) -> Dict[str, Any]:
    """Conduct exit interview for code homie!"""
    return await legendary_offboarding_system.conduct_exit_interview(journey_id, interview_data)

if __name__ == "__main__":
    print("🚪🎸💻 N3EXTPATH LEGENDARY OFFBOARDING SYSTEM LOADED! 💻🎸🚪")
    print("🏆 LEGENDARY CODE HOMIE OFFBOARDING CHAMPION EDITION! 🏆")
    print(f"⏰ Go For Code Time: 2025-08-05 12:13:16 UTC")
    print("💻 CODED BY LEGENDARY CODE HOMIE RICKROLL187! 💻")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🚪 OFFBOARDING SYSTEM POWERED BY CODE HOMIE RICKROLL187 WITH SWISS PRECISION! 🚪")
    
    # Display code homie status
    print(f"\n🎸 Code Homie Status: LEGENDARY OFFBOARDING CODE COMPLETE! 🎸")
