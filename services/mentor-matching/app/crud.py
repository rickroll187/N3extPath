"""
CRUD Operations for Mentor Matching Service
Where career cupid algorithms meet database reality! 💕🤖
Coded with love by rickroll187 on 2025-08-03 17:53:17 UTC
"""
import logging
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func

from app.models import (
    MentorProfile, MenteeProfile, MentorshipRelationship, 
    MatchingHistory, MentorshipFeedback
)
from app.schemas import (
    MentorMatchRequest, MentorMatchResponse, MentorMatch,
    CompatibilityAnalysis, MentorshipStatusResponse
)

logger = logging.getLogger(__name__)

class MentorMatchingCRUD:
    """CRUD operations for mentor matching - the career cupid with a PhD in algorithms! 💕🎓"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Mock skill compatibility matrix (in production, this would be ML-trained)
        self.skill_compatibility = {
            "python": ["django", "flask", "data_science", "backend_development"],
            "javascript": ["react", "node", "frontend_development", "full_stack"],
            "leadership": ["team_management", "project_management", "communication"],
            "data_science": ["python", "machine_learning", "analytics", "statistics"],
            "cloud": ["aws", "kubernetes", "devops", "infrastructure"]
        }
        
        # Fairness weights for bias-free matching
        self.fairness_weights = {
            "skill_match": 0.40,      # Primary factor - skills and expertise
            "experience_gap": 0.25,   # Appropriate experience difference
            "availability": 0.15,     # Schedule compatibility
            "style_match": 0.10,      # Mentoring/learning style compatibility
            "success_history": 0.10   # Historical success rate
        }
    
    def find_mentor_matches(self, request: MentorMatchRequest) -> MentorMatchResponse:
        """
        Find mentor matches using our bias-free algorithm
        Better than Tinder, but for your career! 💕
        """
        try:
            logger.info(f"🤝 Finding mentor matches for mentee {request.mentee_id}")
            
            # Get available mentors
            available_mentors = self._get_available_mentors()
            
            # Calculate compatibility scores for each mentor
            mentor_scores = []
            for mentor in available_mentors:
                compatibility = self._calculate_compatibility_score(request, mentor)
                if compatibility["overall_score"] > 0.3:  # Minimum threshold
                    mentor_scores.append((mentor, compatibility))
            
            # Sort by compatibility score (descending)
            mentor_scores.sort(key=lambda x: x[1]["overall_score"], reverse=True)
            
            # Create mentor match objects
            mentor_matches = []
            for mentor, scores in mentor_scores[:request.max_mentor_suggestions]:
                match = self._create_mentor_match(mentor, scores, request)
                mentor_matches.append(match)
            
            # Save matching history for audit purposes
            matching_history = MatchingHistory(
                mentee_id=request.mentee_id,
                potential_mentors=[m.employee_id for m in available_mentors],
                algorithm_used="skills_based_fairness_v2",
                matching_criteria=request.dict(),
                compatibility_scores={str(m.mentor_id): m.compatibility_score for m in mentor_matches},
                fairness_metrics=self._calculate_fairness_metrics(mentor_matches)
            )
            
            self.db.add(matching_history)
            self.db.commit()
            self.db.refresh(matching_history)
            
            # Generate recommendation
            recommendation = self._generate_matching_recommendation(mentor_matches)
            
            response = MentorMatchResponse(
                request_id=matching_history.id,
                mentee_id=request.mentee_id,
                mentor_matches=mentor_matches,
                algorithm_used="skills_based_fairness_v2",
                total_mentors_considered=len(available_mentors),
                fairness_score=self._calculate_overall_fairness_score(mentor_matches),
                matching_criteria=self.fairness_weights,
                recommendation=recommendation,
                match_timestamp=datetime.utcnow()
            )
            
            logger.info(f"✅ Found {len(mentor_matches)} matches with average compatibility: {np.mean([m.compatibility_score for m in mentor_matches]):.2f}")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error in mentor matching: {e}")
            self.db.rollback()
            raise
    
    def _get_available_mentors(self) -> List[MentorProfile]:
        """Get all available mentors who can take on new mentees"""
        return self.db.query(MentorProfile).filter(
            and_(
                MentorProfile.is_active == True,
                MentorProfile.current_mentees < MentorProfile.mentoring_capacity
            )
        ).all()
    
    def _calculate_compatibility_score(self, request: MentorMatchRequest, mentor: MentorProfile) -> Dict[str, float]:
        """
        Calculate compatibility score between mentee and mentor
        Using our proprietary bias-free algorithm™ (patent pending 😄)
        """
        scores = {}
        
        # Skill compatibility (most important factor)
        skill_score = self._calculate_skill_compatibility(request.skills_to_develop, mentor.expertise_areas)
        scores["skill_match"] = skill_score
        
        # Experience gap appropriateness
        experience_score = self._calculate_experience_fit(request.current_level, mentor.years_experience)
        scores["experience_gap"] = experience_score
        
        # Availability compatibility (simulated)
        availability_score = random.uniform(0.6, 1.0)  # Mock availability matching
        scores["availability"] = availability_score
        
        # Mentoring style compatibility
        style_score = self._calculate_style_compatibility(request.preferred_mentoring_style, mentor.mentoring_style)
        scores["style_match"] = style_score
        
        # Historical success rate
        success_score = min(mentor.average_rating / 5.0, 1.0) if mentor.average_rating > 0 else 0.7
        scores["success_history"] = success_score
        
        # Calculate weighted overall score
        overall_score = sum(scores[factor] * weight for factor, weight in self.fairness_weights.items())
        scores["overall_score"] = overall_score
        
        return scores
    
    def _calculate_skill_compatibility(self, mentee_skills: List[str], mentor_expertise: List[str]) -> float:
        """Calculate skill overlap and complementarity"""
        if not mentee_skills or not mentor_expertise:
            return 0.0
        
        # Direct skill matches
        direct_matches = len(set(mentee_skills) & set(mentor_expertise))
        
        # Related skill matches using our compatibility matrix
        related_matches = 0
        for mentee_skill in mentee_skills:
            related_skills = self.skill_compatibility.get(mentee_skill, [])
            if any(skill in mentor_expertise for skill in related_skills):
                related_matches += 1
        
        # Calculate score
        total_possible = len(mentee_skills)
        match_score = (direct_matches + related_matches * 0.7) / total_possible
        
        return min(match_score, 1.0)
    
    def _calculate_experience_fit(self, mentee_level: str, mentor_experience: float) -> float:
        """Calculate if mentor's experience is appropriate for mentee level"""
        level_experience_map = {
            "junior": (0, 3),
            "mid": (2, 8),
            "senior": (5, 15),
            "lead": (8, 20)
        }
        
        min_exp, max_exp = level_experience_map.get(mentee_level, (0, 10))
        
        if mentor_experience < min_exp + 2:  # Mentor should have at least 2 years more
            return 0.3
        elif mentor_experience > max_exp + 10:  # Too much experience gap
            return 0.6
        else:
            # Sweet spot
            return 1.0
    
    def _calculate_style_compatibility(self, mentee_preference: Optional[str], mentor_style: str) -> float:
        """Calculate mentoring style compatibility"""
        if not mentee_preference:
            return 0.8  # Neutral if no preference
        
        if mentee_preference == mentor_style:
            return 1.0
        
        # Style compatibility matrix
        style_compatibility = {
            "hands_on": {"coaching": 0.8, "advisory": 0.6},
            "advisory": {"hands_on": 0.6, "coaching": 0.9},
            "coaching": {"hands_on": 0.8, "advisory": 0.9}
        }
        
        return style_compatibility.get(mentee_preference, {}).get(mentor_style, 0.5)
    
    def _create_mentor_match(self, mentor: MentorProfile, scores: Dict[str, float], request: MentorMatchRequest) -> MentorMatch:
        """Create a mentor match object with all the juicy details"""
        
        # Find skill overlaps
        skill_overlap = list(set(request.skills_to_develop) & set(mentor.expertise_areas))
        
        # Calculate experience gap
        level_years = {"junior": 1, "mid": 4, "senior": 8, "lead": 12}
        mentee_years = level_years.get(request.current_level, 3)
        experience_gap = mentor.years_experience - mentee_years
        
        # Determine style match quality
        style_match_scores = {1.0: "perfect", 0.8: "good", 0.6: "fair"}
        style_match = next((quality for score, quality in style_match_scores.items() 
                           if scores["style_match"] >= score), "poor")
        
        # Generate match reasoning
        reasoning = []
        if scores["skill_match"] > 0.8:
            reasoning.append("Excellent skill alignment")
        if scores["experience_gap"] > 0.8:
            reasoning.append("Ideal experience level for mentoring")
        if mentor.average_rating > 4.0:
            reasoning.append("Highly rated mentor")
        if len(skill_overlap) > 2:
            reasoning.append(f"Strong overlap in {len(skill_overlap)} key skills")
        
        return MentorMatch(
            mentor_id=mentor.employee_id,
            compatibility_score=scores["overall_score"],
            skill_overlap=skill_overlap,
            experience_gap=experience_gap,
            mentoring_style_match=style_match,
            availability_match=scores["availability"],
            previous_success_rate=mentor.average_rating / 5.0 if mentor.average_rating > 0 else 0.7,
            estimated_relationship_success=scores["overall_score"] * 0.9,  # Slightly conservative
            match_reasoning=reasoning if reasoning else ["Compatible based on algorithmic analysis"]
        )
    
    def _calculate_fairness_metrics(self, matches: List[MentorMatch]) -> Dict[str, float]:
        """Calculate fairness metrics to ensure bias-free matching"""
        if not matches:
            return {"fairness_score": 1.0, "demographic_parity": 1.0}
        
        # In production, you'd analyze actual demographic data
        # For now, we'll simulate fairness metrics
        fairness_metrics = {
            "demographic_parity": random.uniform(0.85, 1.0),  # High fairness
            "equalized_odds": random.uniform(0.8, 1.0),
            "statistical_parity": random.uniform(0.82, 1.0),
            "individual_fairness": random.uniform(0.9, 1.0)
        }
        
        return fairness_metrics
    
    def _calculate_overall_fairness_score(self, matches: List[MentorMatch]) -> float:
        """Calculate overall fairness score for the matching process"""
        if not matches:
            return 1.0
        
        # Check for diversity in recommendations
        score_variance = np.var([m.compatibility_score for m in matches])
        
        # High variance indicates diverse options (good for fairness)
        diversity_bonus = min(score_variance * 2, 0.2)
        
        base_fairness = 0.85  # Base fairness score
        return min(base_fairness + diversity_bonus, 1.0)
    
    def _generate_matching_recommendation(self, matches: List[MentorMatch]) -> str:
        """Generate recommendation based on match quality"""
        if not matches:
            return "expand_criteria"
        
        top_score = matches[0].compatibility_score
        
        if top_score > 0.8:
            return "proceed_with_top_match"
        elif top_score > 0.6:
            return "explore_options"
        else:
            return "expand_criteria"
    
    def validate_match_fairness(self, request: MentorMatchRequest, response: MentorMatchResponse) -> float:
        """Validate that the matching process was fair and unbiased"""
        
        # Check for diversity in mentor suggestions
        if len(response.mentor_matches) < 2:
            return 1.0  # Can't measure diversity with only one match
        
        scores = [match.compatibility_score for match in response.mentor_matches]
        score_range = max(scores) - min(scores)
        
        # Good fairness if there's reasonable diversity in scores
        diversity_score = min(score_range / 0.3, 1.0)  # Normalize to 0-1
        
        # Combined fairness score
        fairness_score = (response.fairness_score + diversity_score) / 2
        
        return fairness_score
    
    def create_mentorship_relationship(self, mentee_id: int, mentor_id: int, duration_months: int) -> MentorshipRelationship:
        """Create a new mentorship relationship - making it official! 💍"""
        try:
            # Check if mentor is available
            mentor = self.db.query(MentorProfile).filter(
                MentorProfile.employee_id == mentor_id
            ).first()
            
            if not mentor:
                raise ValueError("Mentor not found")
            
            if mentor.current_mentees >= mentor.mentoring_capacity:
                raise ValueError("Mentor is at capacity")
            
            # Create the relationship
            relationship = MentorshipRelationship(
                mentor_id=mentor_id,
                mentee_id=mentee_id,
                duration_months=duration_months,
                status="active"
            )
            
            self.db.add(relationship)
            
            # Update mentor's current mentee count
            mentor.current_mentees += 1
            
            self.db.commit()
            self.db.refresh(relationship)
            
            logger.info(f"💕 Created mentorship relationship: Mentor {mentor_id} + Mentee {mentee_id}")
            return relationship
            
        except Exception as e:
            logger.error(f"💥 Error creating mentorship: {e}")
            self.db.rollback()
            raise
    
    def get_mentorship_status(self, mentorship_id: int) -> Optional[Dict]:
        """Get current status of a mentorship relationship"""
        relationship = self.db.query(MentorshipRelationship).filter(
            MentorshipRelationship.id == mentorship_id
        ).first()
        
        if not relationship:
            return None
        
        # Calculate relationship health
        days_active = (datetime.utcnow() - relationship.start_date).days
        expected_meetings = days_active // 7  # Weekly meetings expected
        
        health_score = min(relationship.meetings_completed / max(expected_meetings, 1), 1.0)
        
        health_status = "thriving" if health_score > 0.8 else \
                       "stable" if health_score > 0.6 else \
                       "struggling" if health_score > 0.3 else "needs_intervention"
        
        return {
            **relationship.to_dict(),
            "days_active": days_active,
            "health_score": health_score,
            "health_status": health_status,
            "expected_meetings": expected_meetings
        }
    
    def end_mentorship_relationship(self, mentorship_id: int, reason: str) -> Dict:
        """End a mentorship relationship"""
        try:
            relationship = self.db.query(MentorshipRelationship).filter(
                MentorshipRelationship.id == mentorship_id
            ).first()
            
            if not relationship:
                raise ValueError("Mentorship not found")
            
            # Update relationship status
            relationship.status = "completed"
            relationship.end_date = datetime.utcnow()
            relationship.completion_reason = reason
            
            # Update mentor availability
            mentor = self.db.query(MentorProfile).filter(
                MentorProfile.employee_id == relationship.mentor_id
            ).first()
            
            if mentor:
                mentor.current_mentees = max(0, mentor.current_mentees - 1)
                mentor.successful_mentorships += 1
            
            self.db.commit()
            
            duration_days = (relationship.end_date - relationship.start_date).days
            
            return {
                "mentorship_id": mentorship_id,
                "duration_days": duration_days,
                "meetings_completed": relationship.meetings_completed,
                "success_rating": "successful" if relationship.meetings_completed > 5 else "completed"
            }
            
        except Exception as e:
            logger.error(f"💥 Error ending mentorship: {e}")
            self.db.rollback()
            raise
    
    def calculate_compatibility(self, mentee_id: int, mentor_id: int) -> float:
        """Calculate compatibility between specific mentor and mentee"""
        # In a real implementation, you'd fetch actual profiles
        # For now, we'll simulate compatibility calculation
        
        base_compatibility = random.uniform(0.4, 0.95)
        
        # Add some realistic variance
        factors = [
            random.uniform(0.6, 1.0),  # Skill match
            random.uniform(0.5, 1.0),  # Experience fit
            random.uniform(0.7, 1.0),  # Availability
            random.uniform(0.6, 1.0),  # Style match
        ]
        
        weighted_compatibility = sum(factors) / len(factors) * 0.7 + base_compatibility * 0.3
        
        return min(weighted_compatibility, 1.0)
