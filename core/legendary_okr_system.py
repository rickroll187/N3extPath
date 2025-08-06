"""
🎯🎸 N3EXTPATH - LEGENDARY OKR MANAGEMENT SYSTEM 🎸🎯
More goal-oriented than Swiss precision with legendary OKR mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Logical build time: 2025-08-05 12:48:54 UTC
Built by legendary logical RICKROLL187 🎸🎯
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
import uuid
from decimal import Decimal

class OKRStatus(Enum):
    """🎯 LEGENDARY OKR STATUS! 🎯"""
    DRAFT = "draft"
    ACTIVE = "active" 
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERACHIEVED = "overachieved"
    RICKROLL187_LEGENDARY = "rickroll187_legendary"

class OKRPeriod(Enum):
    """📅 LEGENDARY OKR PERIODS! 📅"""
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"
    CUSTOM = "custom"

class KeyResultType(Enum):
    """🔑 LEGENDARY KEY RESULT TYPES! 🔑"""
    NUMERIC = "numeric"  # Increase X from Y to Z
    PERCENTAGE = "percentage"  # Achieve X% of Y
    BOOLEAN = "boolean"  # Complete X (yes/no)
    MILESTONE = "milestone"  # Launch X by date Y

class AlignmentLevel(Enum):
    """🎯 LEGENDARY ALIGNMENT LEVELS! 🎯"""
    COMPANY = "company"
    DEPARTMENT = "department" 
    TEAM = "team"
    INDIVIDUAL = "individual"
    RICKROLL187_STRATEGIC = "rickroll187_strategic"

@dataclass
class KeyResult:
    """🔑 LEGENDARY KEY RESULT! 🔑"""
    key_result_id: str
    name: str
    description: str
    key_result_type: KeyResultType
    target_value: float
    current_value: float = 0.0
    unit: str = ""  # %, $, count, etc.
    weight: float = 1.0  # Relative importance (0.1 to 2.0)
    due_date: datetime
    status: OKRStatus = OKRStatus.ACTIVE
    completion_percentage: float = 0.0
    updates: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    legendary_factor: str = "LEGENDARY KEY RESULT!"

@dataclass
class Objective:
    """🎯 LEGENDARY OBJECTIVE! 🎯"""
    objective_id: str
    name: str
    description: str
    owner_id: str
    owner_name: str
    alignment_level: AlignmentLevel
    parent_objective_id: Optional[str] = None
    key_results: List[KeyResult] = field(default_factory=list)
    period: OKRPeriod = OKRPeriod.QUARTERLY
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=90))
    status: OKRStatus = OKRStatus.DRAFT
    progress_percentage: float = 0.0
    confidence_level: int = 5  # 1-10 scale of confidence in achieving
    tags: List[str] = field(default_factory=list)
    collaborators: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    rickroll187_approved: bool = False
    legendary_factor: str = "LEGENDARY OBJECTIVE!"

@dataclass
class OKRUpdate:
    """📊 LEGENDARY OKR UPDATE! 📊"""
    update_id: str
    objective_id: str
    key_result_id: Optional[str] = None
    updated_by: str
    update_type: str = "progress"  # progress, milestone, blocker, completion
    previous_value: float = 0.0
    new_value: float = 0.0
    notes: str = ""
    confidence_change: int = 0  # Change in confidence level
    blockers: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    legendary_factor: str = "LEGENDARY UPDATE!"

class LegendaryOKRSystem:
    """
    🎯 THE LEGENDARY OKR MANAGEMENT SYSTEM! 🎯
    More goal-oriented than Swiss precision with logical code bro excellence! 🎸⚡
    """
    
    def __init__(self):
        self.logical_time = "2025-08-05 12:48:54 UTC"
        self.objectives: Dict[str, Objective] = {}
        self.okr_updates: List[OKRUpdate] = []
        
        # OKR scoring system (Google-style)
        self.scoring_system = {
            "excellent": {"min": 0.7, "color": "green", "message": "🏆 LEGENDARY ACHIEVEMENT!"},
            "good": {"min": 0.4, "color": "yellow", "message": "💪 SOLID PROGRESS!"},
            "needs_attention": {"min": 0.0, "color": "red", "message": "🚨 NEEDS FOCUS!"}
        }
        
        # Default OKR templates
        self.okr_templates = {
            "sales": {
                "objective": "Increase Sales Performance",
                "key_results": [
                    {"name": "Achieve Revenue Target", "type": "numeric", "target": 1000000, "unit": "$"},
                    {"name": "Improve Close Rate", "type": "percentage", "target": 25, "unit": "%"},
                    {"name": "Add New Clients", "type": "numeric", "target": 50, "unit": "clients"}
                ]
            },
            "engineering": {
                "objective": "Deliver Legendary Technical Excellence",
                "key_results": [
                    {"name": "Reduce System Downtime", "type": "percentage", "target": 99.9, "unit": "%"},
                    {"name": "Complete Feature Releases", "type": "numeric", "target": 12, "unit": "features"},
                    {"name": "Improve Code Coverage", "type": "percentage", "target": 85, "unit": "%"}
                ]
            },
            "hr": {
                "objective": "Build Legendary Team Culture",
                "key_results": [
                    {"name": "Employee Satisfaction Score", "type": "percentage", "target": 90, "unit": "%"},
                    {"name": "Reduce Turnover Rate", "type": "percentage", "target": 5, "unit": "%"},
                    {"name": "Complete Training Programs", "type": "numeric", "target": 100, "unit": "employees"}
                ]
            }
        }
        
        self.logical_jokes = [
            "Why are OKRs legendary at 12:48:54? Because RICKROLL187 builds goal systems with Swiss precision timing! 🎯🎸",
            "What's more focused than Swiss engineering? Legendary OKRs after logical analysis planning! 🎯⚡",
            "Why don't code bros miss their targets? Because they track OKRs with legendary goal precision! 💪🎯",
            "What do you call perfect logical OKR system? A RICKROLL187 goal achievement special! 🎸🎯"
        ]
    
    async def create_objective(self, objective_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create legendary objective with Swiss precision!
        More goal-oriented than Swiss planning with logical objective creation! 🎯🎸
        """
        objective_id = str(uuid.uuid4())
        
        # Special handling for RICKROLL187 objectives
        if objective_data.get("owner_id") == "rickroll187":
            alignment_level = AlignmentLevel.RICKROLL187_STRATEGIC
            rickroll187_approved = True
            status = OKRStatus.RICKROLL187_LEGENDARY
        else:
            alignment_level = AlignmentLevel(objective_data.get("alignment_level", "individual"))
            rickroll187_approved = False
            status = OKRStatus.DRAFT
        
        # Create key results from templates or custom data
        key_results = []
        if objective_data.get("use_template"):
            template_name = objective_data.get("template_name", "engineering")
            if template_name in self.okr_templates:
                template = self.okr_templates[template_name]
                for kr_template in template["key_results"]:
                    key_result = KeyResult(
                        key_result_id=str(uuid.uuid4()),
                        name=kr_template["name"],
                        description=f"Key result for {template['objective']}",
                        key_result_type=KeyResultType(kr_template["type"]),
                        target_value=kr_template["target"],
                        unit=kr_template["unit"],
                        due_date=datetime.fromisoformat(objective_data.get("end_date", (datetime.utcnow() + timedelta(days=90)).isoformat())),
                        legendary_factor=f"LEGENDARY {kr_template['name'].upper()}! 🔑🏆"
                    )
                    key_results.append(key_result)
        
        # Add custom key results
        for kr_data in objective_data.get("key_results", []):
            key_result = KeyResult(
                key_result_id=str(uuid.uuid4()),
                name=kr_data["name"],
                description=kr_data.get("description", ""),
                key_result_type=KeyResultType(kr_data["type"]),
                target_value=kr_data["target_value"],
                unit=kr_data.get("unit", ""),
                weight=kr_data.get("weight", 1.0),
                due_date=datetime.fromisoformat(kr_data.get("due_date", objective_data.get("end_date", (datetime.utcnow() + timedelta(days=90)).isoformat()))),
                legendary_factor=f"LEGENDARY {kr_data['name'].upper()}! 🔑🏆"
            )
            key_results.append(key_result)
        
        # Create objective
        objective = Objective(
            objective_id=objective_id,
            name=objective_data["name"],
            description=objective_data.get("description", ""),
            owner_id=objective_data["owner_id"],
            owner_name=objective_data.get("owner_name", objective_data["owner_id"]),
            alignment_level=alignment_level,
            parent_objective_id=objective_data.get("parent_objective_id"),
            key_results=key_results,
            period=OKRPeriod(objective_data.get("period", "quarterly")),
            start_date=datetime.fromisoformat(objective_data.get("start_date", datetime.utcnow().isoformat())),
            end_date=datetime.fromisoformat(objective_data.get("end_date", (datetime.utcnow() + timedelta(days=90)).isoformat())),
            status=status,
            confidence_level=objective_data.get("confidence_level", 5),
            tags=objective_data.get("tags", []),
            collaborators=objective_data.get("collaborators", []),
            rickroll187_approved=rickroll187_approved,
            legendary_factor=f"LEGENDARY OBJECTIVE FOR {objective_data['owner_name'].upper()}! 🎯🏆"
        )
        
        self.objectives[objective_id] = objective
        
        import random
        return {
            "success": True,
            "objective_id": objective_id,
            "message": f"🎯 Legendary objective '{objective_data['name']}' created! 🎯",
            "owner": objective_data.get("owner_name", objective_data["owner_id"]),
            "key_results_count": len(key_results),
            "period": objective.period.value,
            "alignment_level": alignment_level.value,
            "status": status.value,
            "created_at": self.logical_time,
            "created_by": "RICKROLL187's Legendary OKR System 🎸🎯",
            "legendary_status": "🎸 RICKROLL187 STRATEGIC OBJECTIVE!" if rickroll187_approved else "LEGENDARY OBJECTIVE CREATED! 🏆",
            "legendary_joke": random.choice(self.logical_jokes)
        }
    
    async def update_key_result_progress(self, objective_id: str, key_result_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update key result progress with legendary precision!
        More accurate than Swiss measurements with logical progress tracking! 📊🎸
        """
        if objective_id not in self.objectives:
            return {
                "success": False,
                "message": "Objective not found!",
                "legendary_message": "This objective doesn't exist in our legendary system! 🔍"
            }
        
        objective = self.objectives[objective_id]
        key_result = None
        
        # Find the key result
        for kr in objective.key_results:
            if kr.key_result_id == key_result_id:
                key_result = kr
                break
        
        if not key_result:
            return {
                "success": False,
                "message": "Key result not found!",
                "legendary_message": "This key result doesn't exist in the legendary objective! 🔑"
            }
        
        # Store previous value for tracking
        previous_value = key_result.current_value
        
        # Update the key result
        key_result.current_value = update_data["new_value"]
        key_result.updated_at = datetime.utcnow()
        
        # Calculate completion percentage
        if key_result.key_result_type == KeyResultType.BOOLEAN:
            key_result.completion_percentage = 100.0 if update_data["new_value"] == 1 else 0.0
        else:
            key_result.completion_percentage = min((key_result.current_value / key_result.target_value) * 100, 100.0)
        
        # Update key result status based on completion
        if key_result.completion_percentage >= 100:
            if key_result.current_value > key_result.target_value:
                key_result.status = OKRStatus.OVERACHIEVED
            else:
                key_result.status = OKRStatus.COMPLETED
        elif key_result.completion_percentage > 0:
            key_result.status = OKRStatus.ACTIVE
        
        # Add update to history
        key_result.updates.append({
            "timestamp": datetime.utcnow().isoformat(),
            "previous_value": previous_value,
            "new_value": update_data["new_value"],
            "updated_by": update_data.get("updated_by", "system"),
            "notes": update_data.get("notes", ""),
            "completion_percentage": key_result.completion_percentage
        })
        
        # Recalculate objective progress
        objective.progress_percentage = await self._calculate_objective_progress(objective)
        objective.updated_at = datetime.utcnow()
        
        # Create update record
        update_record = OKRUpdate(
            update_id=str(uuid.uuid4()),
            objective_id=objective_id,
            key_result_id=key_result_id,
            updated_by=update_data.get("updated_by", "system"),
            update_type="progress",
            previous_value=previous_value,
            new_value=update_data["new_value"],
            notes=update_data.get("notes", ""),
            confidence_change=update_data.get("confidence_change", 0),
            blockers=update_data.get("blockers", []),
            achievements=update_data.get("achievements", []),
            next_steps=update_data.get("next_steps", []),
            legendary_factor=f"LEGENDARY PROGRESS UPDATE FOR {key_result.name.upper()}! 📊🏆"
        )
        
        self.okr_updates.append(update_record)
        
        # Determine scoring
        score_category = self._get_score_category(key_result.completion_percentage / 100)
        
        return {
            "success": True,
            "objective_id": objective_id,
            "key_result_id": key_result_id,
            "key_result_name": key_result.name,
            "previous_value": previous_value,
            "new_value": key_result.current_value,
            "target_value": key_result.target_value,
            "completion_percentage": key_result.completion_percentage,
            "key_result_status": key_result.status.value,
            "objective_progress": objective.progress_percentage,
            "score_category": score_category,
            "scoring_message": self.scoring_system[score_category]["message"],
            "updated_at": self.logical_time,
            "updated_by": f"{update_data.get('updated_by', 'system')} via RICKROLL187's Legendary OKR System 🎸📊",
            "legendary_status": "KEY RESULT UPDATED WITH LEGENDARY PRECISION! 🔑🏆"
        }
    
    async def get_okr_dashboard(self, user_id: str, period: str = "current") -> Dict[str, Any]:
        """
        Get comprehensive OKR dashboard!
        More insightful than Swiss analytics with logical dashboard excellence! 📊🎸
        """
        # Filter objectives for the user
        user_objectives = [obj for obj in self.objectives.values() if obj.owner_id == user_id or user_id in obj.collaborators]
        
        # Calculate dashboard metrics
        total_objectives = len(user_objectives)
        active_objectives = len([obj for obj in user_objectives if obj.status == OKRStatus.ACTIVE])
        completed_objectives = len([obj for obj in user_objectives if obj.status == OKRStatus.COMPLETED])
        
        # Calculate overall progress
        if user_objectives:
            overall_progress = sum([obj.progress_percentage for obj in user_objectives]) / len(user_objectives)
        else:
            overall_progress = 0.0
        
        # Get top performing and at-risk objectives
        top_performing = sorted(user_objectives, key=lambda x: x.progress_percentage, reverse=True)[:3]
        at_risk = [obj for obj in user_objectives if obj.progress_percentage < 30 and obj.status == OKRStatus.ACTIVE]
        
        # Calculate confidence trends
        avg_confidence = sum([obj.confidence_level for obj in user_objectives]) / len(user_objectives) if user_objectives else 5
        
        # Recent updates
        user_updates = [update for update in self.okr_updates 
                       if any(obj.objective_id == update.objective_id for obj in user_objectives)][-10:]  # Last 10 updates
        
        dashboard = {
            "dashboard_title": f"🎯 LEGENDARY OKR DASHBOARD - {user_id.upper()} 🎯",
            "period": period,
            "generated_at": self.logical_time,
            "generated_for": user_id,
            
            "summary_metrics": {
                "total_objectives": total_objectives,
                "active_objectives": active_objectives,
                "completed_objectives": completed_objectives,
                "overall_progress": round(overall_progress, 1),
                "average_confidence": round(avg_confidence, 1),
                "completion_rate": round((completed_objectives / total_objectives * 100), 1) if total_objectives > 0 else 0
            },
            
            "progress_breakdown": {
                "on_track": len([obj for obj in user_objectives if obj.progress_percentage >= 70]),
                "needs_attention": len([obj for obj in user_objectives if 30 <= obj.progress_percentage < 70]),
                "at_risk": len(at_risk)
            },
            
            "top_performing_objectives": [
                {
                    "objective_id": obj.objective_id,
                    "name": obj.name,
                    "progress": obj.progress_percentage,
                    "status": obj.status.value,
                    "key_results_count": len(obj.key_results)
                }
                for obj in top_performing
            ],
            
            "at_risk_objectives": [
                {
                    "objective_id": obj.objective_id,
                    "name": obj.name,
                    "progress": obj.progress_percentage,
                    "confidence": obj.confidence_level,
                    "days_remaining": (obj.end_date - datetime.utcnow()).days
                }
                for obj in at_risk
            ],
            
            "recent_updates": [
                {
                    "update_type": update.update_type,
                    "objective_name": next((obj.name for obj in user_objectives if obj.objective_id == update.objective_id), "Unknown"),
                    "notes": update.notes,
                    "timestamp": update.timestamp.isoformat(),
                    "updated_by": update.updated_by
                }
                for update in user_updates
            ],
            
            "recommendations": await self._generate_okr_recommendations(user_objectives),
            
            "legendary_insights": [
                f"🎸 {user_id} is tracking {total_objectives} legendary objectives!",
                f"🏆 Overall progress of {overall_progress:.1f}% shows solid momentum!",
                f"💪 Confidence level of {avg_confidence:.1f}/10 indicates strong commitment!",
                f"⚡ {active_objectives} objectives actively driving towards legendary results!"
            ],
            
            "rickroll187_personal_note": f"🎸 Keep crushing those OKRs, {user_id}! Your legendary goal-setting inspires the whole team! 🎸" if user_id != "rickroll187" else "🎸 The legendary founder's OKRs are shaping our entire universe! 🎸"
        }
        
        return dashboard
    
    async def _calculate_objective_progress(self, objective: Objective) -> float:
        """Calculate weighted progress for objective based on key results!"""
        if not objective.key_results:
            return 0.0
        
        total_weighted_progress = 0.0
        total_weight = 0.0
        
        for kr in objective.key_results:
            progress = kr.completion_percentage / 100.0
            weight = kr.weight
            total_weighted_progress += progress * weight
            total_weight += weight
        
        return (total_weighted_progress / total_weight) * 100 if total_weight > 0 else 0.0
    
    def _get_score_category(self, score: float) -> str:
        """Get OKR score category based on completion percentage!"""
        if score >= self.scoring_system["excellent"]["min"]:
            return "excellent"
        elif score >= self.scoring_system["good"]["min"]:
            return "good"
        else:
            return "needs_attention"
    
    async def _generate_okr_recommendations(self, objectives: List[Objective]) -> List[str]:
        """Generate personalized OKR recommendations!"""
        recommendations = []
        
        if not objectives:
            recommendations.append("🎯 Start by creating your first legendary objective!")
            return recommendations
        
        # Check for at-risk objectives
        at_risk = [obj for obj in objectives if obj.progress_percentage < 30]
        if at_risk:
            recommendations.append(f"🚨 Focus on {len(at_risk)} at-risk objectives - consider breaking down into smaller milestones")
        
        # Check for low confidence
        low_confidence = [obj for obj in objectives if obj.confidence_level <= 3]
        if low_confidence:
            recommendations.append(f"💪 Boost confidence in {len(low_confidence)} objectives - identify and address blockers")
        
        # Check for completion opportunities
        near_complete = [obj for obj in objectives if 80 <= obj.progress_percentage < 100]
        if near_complete:
            recommendations.append(f"🏆 Push {len(near_complete)} objectives over the finish line - you're almost there!")
        
        # General recommendations
        avg_progress = sum([obj.progress_percentage for obj in objectives]) / len(objectives)
        if avg_progress > 70:
            recommendations.append("🌟 Excellent overall progress! Consider setting stretch goals for next period")
        elif avg_progress < 40:
            recommendations.append("📈 Focus on key priorities - consider reducing scope to ensure quality delivery")
        
        return recommendations

# Global legendary OKR system
legendary_okr_system = LegendaryOKRSystem()

# Logical convenience functions
async def create_legendary_objective(objective_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create objective with logical precision!"""
    return await legendary_okr_system.create_objective(objective_data)

async def update_legendary_progress(objective_id: str, key_result_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update progress with logical tracking!"""
    return await legendary_okr_system.update_key_result_progress(objective_id, key_result_id, update_data)

async def get_legendary_okr_dashboard(user_id: str) -> Dict[str, Any]:
    """Get OKR dashboard with logical insights!"""
    return await legendary_okr_system.get_okr_dashboard(user_id)

if __name__ == "__main__":
    print("🎯🎸💻 N3EXTPATH LEGENDARY OKR MANAGEMENT SYSTEM LOADED! 💻🎸🎯")
    print("🏆 LEGENDARY LOGICAL OKR CHAMPION EDITION! 🏆")
    print(f"⏰ Logical Build Time: 2025-08-05 12:48:54 UTC")
    print("💻 LOGICALLY CODED BY LEGENDARY RICKROLL187! 💻")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🎯 OKR SYSTEM POWERED BY LOGICAL RICKROLL187 WITH SWISS GOAL PRECISION! 🎯")
    
    # Display logical status
    print(f"\n🎸 Logical Code Status: LEGENDARY OKR SYSTEM COMPLETE! 🎸")
