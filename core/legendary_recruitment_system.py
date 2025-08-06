"""
🔍🎸 N3EXTPATH - LEGENDARY TALENT ACQUISITION SYSTEM 🎸🔍
More precise than Swiss headhunting with legendary recruitment mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Architecture time: 2025-08-05 12:07:28 UTC
Built by fresh and legendary RICKROLL187 🎸
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import uuid

class CandidateStatus(Enum):
    """🔍 LEGENDARY CANDIDATE STATUS! 🔍"""
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEWING = "interviewing"
    FINAL_REVIEW = "final_review"
    OFFER_EXTENDED = "offer_extended"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    RICKROLL187_PRIORITY = "rickroll187_priority"

class InterviewType(Enum):
    """🎤 LEGENDARY INTERVIEW TYPES! 🎤"""
    PHONE_SCREEN = "phone_screen"
    TECHNICAL_INTERVIEW = "technical_interview"
    BEHAVIORAL_INTERVIEW = "behavioral_interview"
    PANEL_INTERVIEW = "panel_interview"
    FINAL_INTERVIEW = "final_interview"
    RICKROLL187_LEGENDARY_CHAT = "rickroll187_legendary_chat"

@dataclass
class Candidate:
    """🔍 LEGENDARY CANDIDATE PROFILE! 🔍"""
    candidate_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    position_applied: str
    department: str
    status: CandidateStatus
    resume_url: str
    application_date: datetime
    source: str  # LinkedIn, referral, job board, etc.
    experience_years: int
    skills: List[str]
    salary_expectation: Optional[int] = None
    availability_date: Optional[datetime] = None
    interview_scores: Dict[str, float] = None
    notes: str = ""
    rickroll187_approved: bool = False
    legendary_potential: bool = False

@dataclass 
class Interview:
    """🎤 LEGENDARY INTERVIEW SESSION! 🎤"""
    interview_id: str
    candidate_id: str
    interview_type: InterviewType
    interviewer_id: str
    scheduled_date: datetime
    duration_minutes: int
    location: str  # Office, Zoom, etc.
    status: str  # scheduled, completed, cancelled
    feedback: str = ""
    score: Optional[float] = None
    recommendation: str = ""  # hire, no_hire, maybe
    completed_date: Optional[datetime] = None
    legendary_factor: str = "LEGENDARY INTERVIEW!"

class LegendaryRecruitmentSystem:
    """
    🔍 THE LEGENDARY TALENT ACQUISITION SYSTEM! 🔍
    More precise than Swiss headhunting with fresh recruitment excellence! 🎸⚡
    """
    
    def __init__(self):
        self.architecture_time = "2025-08-05 12:07:28 UTC"
        self.candidates: Dict[str, Candidate] = {}
        self.interviews: Dict[str, Interview] = {}
        
        # Standard interview process templates
        self.interview_processes = {
            "engineering": [
                InterviewType.PHONE_SCREEN,
                InterviewType.TECHNICAL_INTERVIEW,
                InterviewType.BEHAVIORAL_INTERVIEW,
                InterviewType.FINAL_INTERVIEW
            ],
            "sales": [
                InterviewType.PHONE_SCREEN,
                InterviewType.BEHAVIORAL_INTERVIEW,
                InterviewType.PANEL_INTERVIEW,
                InterviewType.FINAL_INTERVIEW
            ],
            "executive": [
                InterviewType.PHONE_SCREEN,
                InterviewType.BEHAVIORAL_INTERVIEW,
                InterviewType.PANEL_INTERVIEW,
                InterviewType.RICKROLL187_LEGENDARY_CHAT,
                InterviewType.FINAL_INTERVIEW
            ]
        }
        
        self.recruitment_jokes = [
            "Why is recruitment legendary at 12:07:28? Because RICKROLL187 finds code bros with Swiss precision timing! 🔍🎸",
            "What's more selective than Swiss banks? Legendary recruitment after fresh architecture planning! 🏦⚡",
            "Why don't great candidates slip away? Because they get legendary recruitment experience with code bro treatment! 💪🔍",
            "What do you call perfect fresh talent acquisition? A RICKROLL187 headhunting special! 🎸🔍"
        ]
    
    async def add_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new legendary candidate to the system!
        More organized than Swiss precision with fresh candidate management! 🔍🎸
        """
        candidate_id = str(uuid.uuid4())
        
        # Check for legendary potential
        legendary_skills = ["python", "leadership", "problem-solving", "teamwork", "innovation"]
        candidate_skills = [skill.lower() for skill in candidate_data.get("skills", [])]
        legendary_potential = len(set(legendary_skills) & set(candidate_skills)) >= 3
        
        # Special handling for referrals from RICKROLL187
        if candidate_data.get("referred_by") == "rickroll187":
            status = CandidateStatus.RICKROLL187_PRIORITY
            rickroll187_approved = True
        else:
            status = CandidateStatus.APPLIED
            rickroll187_approved = False
        
        candidate = Candidate(
            candidate_id=candidate_id,
            first_name=candidate_data["first_name"],
            last_name=candidate_data["last_name"],
            email=candidate_data["email"],
            phone=candidate_data["phone"],
            position_applied=candidate_data["position"],
            department=candidate_data["department"],
            status=status,
            resume_url=candidate_data["resume_url"],
            application_date=datetime.utcnow(),
            source=candidate_data.get("source", "direct_application"),
            experience_years=candidate_data.get("experience_years", 0),
            skills=candidate_data.get("skills", []),
            salary_expectation=candidate_data.get("salary_expectation"),
            availability_date=datetime.fromisoformat(candidate_data["availability_date"]) if candidate_data.get("availability_date") else None,
            interview_scores={},
            rickroll187_approved=rickroll187_approved,
            legendary_potential=legendary_potential
        )
        
        self.candidates[candidate_id] = candidate
        
        # Auto-schedule initial screening if high priority
        if status == CandidateStatus.RICKROLL187_PRIORITY:
            await self._schedule_priority_screening(candidate)
        
        import random
        return {
            "success": True,
            "candidate_id": candidate_id,
            "message": f"🔍 Candidate {candidate.first_name} {candidate.last_name} added to legendary recruitment pipeline! 🔍",
            "status": status.value,
            "legendary_potential": legendary_potential,
            "interview_process": self.interview_processes.get(candidate.department.lower(), self.interview_processes["engineering"]),
            "added_at": self.architecture_time,
            "added_by": "RICKROLL187's Legendary Recruitment System 🎸🔍",
            "legendary_status": "🎸 RICKROLL187 PRIORITY CANDIDATE!" if rickroll187_approved else "LEGENDARY CANDIDATE ADDED TO PIPELINE! 🏆",
            "legendary_joke": random.choice(self.recruitment_jokes)
        }
    
    async def schedule_interview(self, candidate_id: str, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule a legendary interview with precision timing!
        More organized than Swiss calendars with fresh interview scheduling! 🎤🎸
        """
        if candidate_id not in self.candidates:
            return {
                "success": False,
                "message": "Candidate not found!",
                "legendary_message": "This candidate doesn't exist in our legendary recruitment system! 🔍"
            }
        
        interview_id = str(uuid.uuid4())
        candidate = self.candidates[candidate_id]
        
        interview = Interview(
            interview_id=interview_id,
            candidate_id=candidate_id,
            interview_type=InterviewType(interview_data["interview_type"]),
            interviewer_id=interview_data["interviewer_id"],
            scheduled_date=datetime.fromisoformat(interview_data["scheduled_date"]),
            duration_minutes=interview_data.get("duration_minutes", 60),
            location=interview_data.get("location", "Zoom"),
            status="scheduled",
            legendary_factor=f"LEGENDARY {interview_data['interview_type'].upper()} INTERVIEW! 🎤🏆"
        )
        
        self.interviews[interview_id] = interview
        
        # Update candidate status
        if candidate.status == CandidateStatus.APPLIED:
            candidate.status = CandidateStatus.SCREENING
        elif candidate.status in [CandidateStatus.SCREENING, CandidateStatus.INTERVIEWING]:
            candidate.status = CandidateStatus.INTERVIEWING
        
        # Send notifications
        await self._send_interview_notifications(candidate, interview)
        
        return {
            "success": True,
            "interview_id": interview_id,
            "candidate_name": f"{candidate.first_name} {candidate.last_name}",
            "interview_type": interview.interview_type.value,
            "scheduled_date": interview.scheduled_date.isoformat(),
            "interviewer": interview.interviewer_id,
            "message": f"🎤 Interview scheduled for {candidate.first_name} {candidate.last_name}! 🎤",
            "scheduled_at": self.architecture_time,
            "scheduled_by": "RICKROLL187's Legendary Interview Scheduler 🎸🎤",
            "legendary_status": "LEGENDARY INTERVIEW SCHEDULED WITH SWISS PRECISION! ⏰🏆"
        }
    
    async def complete_interview(self, interview_id: str, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete interview with legendary feedback!
        More thorough than Swiss evaluations with fresh interview completion! ✅🎸
        """
        if interview_id not in self.interviews:
            return {
                "success": False,
                "message": "Interview not found!",
                "legendary_message": "This interview doesn't exist in our legendary system! 🎤"
            }
        
        interview = self.interviews[interview_id]
        candidate = self.candidates[interview.candidate_id]
        
        # Update interview with feedback
        interview.status = "completed"
        interview.completed_date = datetime.utcnow()
        interview.feedback = feedback_data.get("feedback", "")
        interview.score = feedback_data.get("score", 0.0)
        interview.recommendation = feedback_data.get("recommendation", "")
        
        # Update candidate interview scores
        if candidate.interview_scores is None:
            candidate.interview_scores = {}
        candidate.interview_scores[interview.interview_type.value] = interview.score
        
        # Calculate overall candidate score
        overall_score = sum(candidate.interview_scores.values()) / len(candidate.interview_scores)
        
        # Determine next steps based on score and recommendation
        if interview.recommendation == "hire" and overall_score >= 4.0:
            candidate.status = CandidateStatus.FINAL_REVIEW
            next_step = "Move to final review and offer preparation"
        elif interview.recommendation == "no_hire" or overall_score < 2.5:
            candidate.status = CandidateStatus.REJECTED
            next_step = "Send rejection email with feedback"
        else:
            next_step = "Continue with next interview in process"
        
        return {
            "success": True,
            "interview_id": interview_id,
            "candidate_name": f"{candidate.first_name} {candidate.last_name}",
            "interview_score": interview.score,
            "overall_candidate_score": round(overall_score, 2),
            "recommendation": interview.recommendation,
            "candidate_status": candidate.status.value,
            "next_step": next_step,
            "completed_at": self.architecture_time,
            "completed_by": "RICKROLL187's Legendary Interview System 🎸✅",
            "legendary_status": "INTERVIEW COMPLETED WITH LEGENDARY THOROUGHNESS! 🎤🏆"
        }
    
    async def _schedule_priority_screening(self, candidate: Candidate):
        """Schedule priority screening for RICKROLL187 referrals!"""
        print(f"🚀 Priority screening scheduled for {candidate.first_name} {candidate.last_name}")
    
    async def _send_interview_notifications(self, candidate: Candidate, interview: Interview):
        """Send interview scheduling notifications!"""
        notifications = [
            f"🎤 Interview scheduled: {candidate.first_name} {candidate.last_name} - {interview.interview_type.value}",
            f"📅 Interviewer {interview.interviewer_id}: You have an interview scheduled for {interview.scheduled_date}",
            f"📧 Candidate notification: Interview confirmation sent to {candidate.email}"
        ]
        
        for notification in notifications:
            print(f"🔔 Interview Notification: {notification}")

# Global legendary recruitment system
legendary_recruitment_system = LegendaryRecruitmentSystem()
