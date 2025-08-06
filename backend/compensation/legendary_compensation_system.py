# File: backend/compensation/legendary_compensation_system.py
"""
💰🎸 N3EXTPATH - LEGENDARY COMPENSATION MANAGEMENT SYSTEM 🎸💰
Professional compensation management with Swiss precision and legendary equity
Built: 2025-08-05 17:45:05 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import json
import uuid
import re
import ast
import operator
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import hashlib
import secrets
import logging
import numpy as np
from scipy import stats

Base = declarative_base()

class CompensationType(Enum):
    """Compensation types with legendary options"""
    BASE_SALARY = "base_salary"
    HOURLY_WAGE = "hourly_wage"
    COMMISSION = "commission"
    BONUS = "bonus"
    EQUITY = "equity"
    BENEFITS = "benefits"
    LEGENDARY_PACKAGE = "legendary_package"  # Special for RICKROLL187

class PayFrequency(Enum):
    """Pay frequency options"""
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    LEGENDARY_CONTINUOUS = "legendary_continuous"  # Real-time for legends

class EquityType(Enum):
    """Equity compensation types"""
    STOCK_OPTIONS = "stock_options"
    RSU = "rsu"
    ESPP = "espp"
    PHANTOM_STOCK = "phantom_stock"
    LEGENDARY_FOUNDER_SHARES = "legendary_founder_shares"

class BonusType(Enum):
    """Bonus calculation types"""
    FIXED_AMOUNT = "fixed_amount"
    PERCENTAGE_SALARY = "percentage_salary"
    PERFORMANCE_BASED = "performance_based"
    PROFIT_SHARING = "profit_sharing"
    LEGENDARY_MULTIPLIER = "legendary_multiplier"

class CompensationStatus(Enum):
    """Compensation record status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SUSPENDED = "suspended"
    LEGENDARY_APPROVED = "legendary_approved"

class MarketDataSource(Enum):
    """Market data sources for benchmarking"""
    RADFORD = "radford"
    MERCER = "mercer"
    PAYSCALE = "payscale"
    GLASSDOOR = "glassdoor"
    LEVELS_FYI = "levels_fyi"
    LEGENDARY_INSIDER = "legendary_insider"

# Database Models
class SalaryBand(Base):
    """Salary bands with market data"""
    __tablename__ = "salary_bands"
    
    band_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    band_name = sa.Column(sa.String(100), nullable=False)
    job_level = sa.Column(sa.String(50))
    department = sa.Column(sa.String(100))
    location = sa.Column(sa.String(100))
    currency = sa.Column(sa.String(3), default="USD")
    min_salary = sa.Column(sa.Numeric(12, 2))
    mid_salary = sa.Column(sa.Numeric(12, 2))
    max_salary = sa.Column(sa.Numeric(12, 2))
    market_percentile = sa.Column(sa.Integer)  # 50th, 75th, 90th percentile
    effective_date = sa.Column(sa.Date)
    expiry_date = sa.Column(sa.Date)
    is_legendary = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

class CompensationPlan(Base):
    """Employee compensation plans"""
    __tablename__ = "compensation_plans"
    
    plan_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = sa.Column(sa.String(36), sa.ForeignKey("users.user_id"))
    plan_name = sa.Column(sa.String(200))
    status = sa.Column(sa.Enum(CompensationStatus), default=CompensationStatus.DRAFT)
    effective_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    currency = sa.Column(sa.String(3), default="USD")
    total_annual_value = sa.Column(sa.Numeric(12, 2))
    approved_by = sa.Column(sa.String(36))
    approved_at = sa.Column(sa.DateTime(timezone=True))
    is_legendary = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relationships
    components = relationship("CompensationComponent", back_populates="plan", cascade="all, delete-orphan")
    history = relationship("CompensationHistory", back_populates="plan")

class CompensationComponent(Base):
    """Individual compensation components"""
    __tablename__ = "compensation_components"
    
    component_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = sa.Column(sa.String(36), sa.ForeignKey("compensation_plans.plan_id"))
    component_type = sa.Column(sa.Enum(CompensationType))
    component_name = sa.Column(sa.String(200))
    base_amount = sa.Column(sa.Numeric(12, 2))
    currency = sa.Column(sa.String(3), default="USD")
    pay_frequency = sa.Column(sa.Enum(PayFrequency))
    is_variable = sa.Column(sa.Boolean, default=False)
    calculation_formula = sa.Column(sa.Text)
    target_percentage = sa.Column(sa.Numeric(5, 2))  # For bonuses
    minimum_amount = sa.Column(sa.Numeric(12, 2))
    maximum_amount = sa.Column(sa.Numeric(12, 2))
    performance_multiplier = sa.Column(sa.Numeric(3, 2), default=1.0)
    is_legendary = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    # Relationships
    plan = relationship("CompensationPlan", back_populates="components")

class EquityGrant(Base):
    """Equity compensation grants"""
    __tablename__ = "equity_grants"
    
    grant_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = sa.Column(sa.String(36), sa.ForeignKey("users.user_id"))
    equity_type = sa.Column(sa.Enum(EquityType))
    grant_date = sa.Column(sa.Date)
    vesting_start_date = sa.Column(sa.Date)
    vesting_cliff_months = sa.Column(sa.Integer, default=12)
    total_vesting_months = sa.Column(sa.Integer, default=48)
    total_shares = sa.Column(sa.Integer)
    strike_price = sa.Column(sa.Numeric(10, 4))
    current_fair_value = sa.Column(sa.Numeric(10, 4))
    vested_shares = sa.Column(sa.Integer, default=0)
    exercised_shares = sa.Column(sa.Integer, default=0)
    is_legendary_grant = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

class BonusCalculation(Base):
    """Bonus calculations and payouts"""
    __tablename__ = "bonus_calculations"
    
    calculation_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = sa.Column(sa.String(36), sa.ForeignKey("users.user_id"))
    bonus_type = sa.Column(sa.Enum(BonusType))
    calculation_period_start = sa.Column(sa.Date)
    calculation_period_end = sa.Column(sa.Date)
    base_amount = sa.Column(sa.Numeric(12, 2))
    performance_score = sa.Column(sa.Numeric(5, 2))
    performance_multiplier = sa.Column(sa.Numeric(3, 2))
    calculated_amount = sa.Column(sa.Numeric(12, 2))
    final_amount = sa.Column(sa.Numeric(12, 2))
    approval_status = sa.Column(sa.String(50), default="pending")
    payout_date = sa.Column(sa.Date)
    is_legendary_bonus = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

class CompensationHistory(Base):
    """Historical compensation changes"""
    __tablename__ = "compensation_history"
    
    history_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = sa.Column(sa.String(36), sa.ForeignKey("compensation_plans.plan_id"))
    user_id = sa.Column(sa.String(36), sa.ForeignKey("users.user_id"))
    change_type = sa.Column(sa.String(100))  # promotion, merit_increase, market_adjustment
    previous_value = sa.Column(sa.Numeric(12, 2))
    new_value = sa.Column(sa.Numeric(12, 2))
    change_percentage = sa.Column(sa.Numeric(5, 2))
    effective_date = sa.Column(sa.Date)
    reason = sa.Column(sa.Text)
    approved_by = sa.Column(sa.String(36))
    approved_at = sa.Column(sa.DateTime(timezone=True))
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    # Relationships
    plan = relationship("CompensationPlan", back_populates="history")

class PayrollRecord(Base):
    """Payroll processing records"""
    __tablename__ = "payroll_records"
    
    payroll_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = sa.Column(sa.String(36), sa.ForeignKey("users.user_id"))
    pay_period_start = sa.Column(sa.Date)
    pay_period_end = sa.Column(sa.Date)
    gross_pay = sa.Column(sa.Numeric(12, 2))
    base_pay = sa.Column(sa.Numeric(12, 2))
    overtime_pay = sa.Column(sa.Numeric(12, 2))
    bonus_pay = sa.Column(sa.Numeric(12, 2))
    commission_pay = sa.Column(sa.Numeric(12, 2))
    deductions = sa.Column(sa.JSON)  # Detailed deductions
    taxes = sa.Column(sa.JSON)  # Tax calculations
    net_pay = sa.Column(sa.Numeric(12, 2))
    pay_date = sa.Column(sa.Date)
    status = sa.Column(sa.String(50), default="processed")
    is_legendary_pay = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

class MarketBenchmark(Base):
    """Market compensation benchmarks"""
    __tablename__ = "market_benchmarks"
    
    benchmark_id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_title = sa.Column(sa.String(200))
    job_level = sa.Column(sa.String(50))
    department = sa.Column(sa.String(100))
    location = sa.Column(sa.String(100))
    company_size = sa.Column(sa.String(50))
    industry = sa.Column(sa.String(100))
    data_source = sa.Column(sa.Enum(MarketDataSource))
    percentile_25 = sa.Column(sa.Numeric(12, 2))
    percentile_50 = sa.Column(sa.Numeric(12, 2))
    percentile_75 = sa.Column(sa.Numeric(12, 2))
    percentile_90 = sa.Column(sa.Numeric(12, 2))
    sample_size = sa.Column(sa.Integer)
    data_date = sa.Column(sa.Date)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

@dataclass
class CompensationSummary:
    """Compensation summary with all components"""
    user_id: str
    base_salary: Decimal
    variable_pay: Decimal
    equity_value: Decimal
    benefits_value: Decimal
    total_compensation: Decimal
    currency: str = "USD"
    is_legendary: bool = False

@dataclass
class PayrollSummary:
    """Payroll processing summary"""
    payroll_id: str
    user_id: str
    pay_period: str
    gross_pay: Decimal
    net_pay: Decimal
    deductions_total: Decimal
    taxes_total: Decimal
    is_legendary: bool = False

class LegendaryCompensationSystem:
    """Professional Compensation Management System with Swiss Precision"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)
        
        # Market data integration
        self.market_data_sources = [
            "Radford", "Mercer", "PayScale", "Glassdoor", "Levels.fyi", "Legendary Insider"
        ]
        
        # Compensation calculation engines
        self.calculation_engines = self._initialize_calculation_engines()
        
        # Equity management
        self.equity_manager = self._initialize_equity_manager()
        
        # Benefits integration
        self.benefits_integration = self._initialize_benefits_integration()
        
        # Tax calculation engine
        self.tax_engine = self._initialize_tax_engine()
        
        # Payroll integration
        self.payroll_engine = self._initialize_payroll_engine()
    
    def _initialize_calculation_engines(self) -> Dict[str, Any]:
        """Initialize compensation calculation engines"""
        
        return {
            "bonus_calculator": {
                "performance_weights": {
                    "individual_performance": 0.6,
                    "team_performance": 0.2,
                    "company_performance": 0.2
                },
                "legendary_multiplier": 2.0,  # 2x bonus for legendary performance
                "swiss_precision_bonus": 0.15  # 15% precision bonus
            },
            
            "equity_calculator": {
                "vesting_schedules": {
                    "standard": {"cliff": 12, "total": 48},
                    "senior": {"cliff": 6, "total": 36},
                    "legendary": {"cliff": 0, "total": 24}  # Instant vesting for legends
                },
                "valuation_methods": ["409a", "black_scholes", "monte_carlo"],
                "legendary_acceleration": True
            },
            
            "market_adjustment": {
                "adjustment_frequency": "quarterly",
                "percentile_targets": {
                    "entry": 50,
                    "experienced": 65,
                    "senior": 75,
                    "legendary": 95
                },
                "cost_of_living_adjustments": True
            },
            
            "salary_formula": {
                "base_multipliers": {
                    "experience": 0.05,  # 5% per year of experience
                    "performance": 0.15,  # Up to 15% for performance
                    "market_position": 0.10,  # Up to 10% for market positioning
                    "legendary_status": 0.50  # 50% legendary premium
                }
            }
        }
    
    def _initialize_equity_manager(self) -> Dict[str, Any]:
        """Initialize equity management system"""
        
        return {
            "company_valuation": Decimal("500000000.00"),  # $500M valuation
            "total_shares": 50000000,
            "option_pool_percentage": 20.0,
            "current_409a_price": Decimal("25.00"),
            "legendary_founder_percentage": 35.0,  # RICKROLL187's stake
            "vesting_acceleration_events": [
                "ipo", "acquisition", "change_of_control", "legendary_milestone"
            ],
            "strike_price_discounts": {
                "employee": 0.0,
                "senior": 0.10,
                "legendary": 0.50  # 50% discount for legends
            }
        }
    
    def _initialize_benefits_integration(self) -> Dict[str, Any]:
        """Initialize benefits integration"""
        
        return {
            "health_insurance": {
                "employee_cost_percentage": 0.15,
                "company_cost_percentage": 0.85,
                "annual_company_cost": 12000,
                "legendary_premium_coverage": True
            },
            "dental_insurance": {
                "employee_cost_percentage": 0.25,
                "company_cost_percentage": 0.75,
                "annual_company_cost": 2400
            },
            "vision_insurance": {
                "employee_cost_percentage": 0.30,
                "company_cost_percentage": 0.70,
                "annual_company_cost": 600
            },
            "retirement_401k": {
                "company_match_percentage": 0.06,
                "max_match_percentage": 0.04,
                "vesting_schedule": "immediate",
                "legendary_bonus_match": 0.02
            },
            "pto_policies": {
                "base_days": 20,
                "senior_days": 25,
                "legendary_days": "unlimited",
                "accrual_rate": 1.67  # days per month
            },
            "legendary_perks": {
                "swiss_precision_bonus": 5000,
                "code_bro_events_budget": 10000,
                "legendary_workspace_allowance": 15000,
                "professional_development": 25000,
                "wellness_stipend": 3000
            }
        }
    
    def _initialize_tax_engine(self) -> Dict[str, Any]:
        """Initialize tax calculation engine"""
        
        return {
            "federal_tax_brackets": [
                {"min": 0, "max": 10275, "rate": 0.10},
                {"min": 10275, "max": 41775, "rate": 0.12},
                {"min": 41775, "max": 89450, "rate": 0.22},
                {"min": 89450, "max": 190750, "rate": 0.24},
                {"min": 190750, "max": 364200, "rate": 0.32},
                {"min": 364200, "max": 462500, "rate": 0.35},
                {"min": 462500, "max": float('inf'), "rate": 0.37}
            ],
            "state_tax_rates": {
                "CA": 0.133,  # California
                "NY": 0.108,  # New York
                "TX": 0.0,    # Texas
                "FL": 0.0,    # Florida
                "WA": 0.0     # Washington
            },
            "payroll_taxes": {
                "social_security": 0.062,
                "medicare": 0.0145,
                "federal_unemployment": 0.006,
                "state_unemployment": 0.024
            },
            "legendary_tax_optimization": True
        }
    
    def _initialize_payroll_engine(self) -> Dict[str, Any]:
        """Initialize payroll processing engine"""
        
        return {
            "pay_schedules": {
                "weekly": 52,
                "bi_weekly": 26,
                "monthly": 12,
                "legendary_continuous": 365  # Daily for legends
            },
            "processing_dates": {
                "cutoff_days_before": 5,
                "processing_days": 2,
                "delivery_method": "direct_deposit"
            },
            "deduction_categories": [
                "health_insurance", "dental_insurance", "vision_insurance",
                "retirement_401k", "life_insurance", "disability_insurance",
                "parking", "transit", "legendary_perks"
            ]
        }
    
    async def create_compensation_plan(self, plan_data: Dict[str, Any], created_by: str) -> Dict[str, Any]:
        """Create comprehensive compensation plan"""
        
        try:
            user_id = plan_data["user_id"]
            
            # Validate authorization
            if not await self._validate_compensation_authority(created_by, user_id):
                return {"success": False, "error": "Insufficient authority to create compensation plan"}
            
            # Create compensation plan
            plan = CompensationPlan(
                user_id=user_id,
                plan_name=plan_data.get("plan_name", f"Compensation Plan - {user_id}"),
                effective_date=datetime.strptime(plan_data["effective_date"], "%Y-%m-%d").date(),
                end_date=datetime.strptime(plan_data["end_date"], "%Y-%m-%d").date() if plan_data.get("end_date") else None,
                currency=plan_data.get("currency", "USD"),
                is_legendary=user_id == "rickroll187" or plan_data.get("is_legendary", False)
            )
            
            self.db_session.add(plan)
            await self.db_session.flush()  # Get plan ID
            
            # Create compensation components
            total_annual_value = Decimal("0.00")
            
            for component_data in plan_data.get("components", []):
                component = CompensationComponent(
                    plan_id=plan.plan_id,
                    component_type=CompensationType(component_data["type"]),
                    component_name=component_data["name"],
                    base_amount=Decimal(str(component_data["amount"])),
                    currency=component_data.get("currency", "USD"),
                    pay_frequency=PayFrequency(component_data.get("frequency", "monthly")),
                    is_variable=component_data.get("is_variable", False),
                    calculation_formula=component_data.get("formula"),
                    target_percentage=Decimal(str(component_data.get("target_percentage", 0))),
                    minimum_amount=Decimal(str(component_data.get("min_amount", 0))),
                    maximum_amount=Decimal(str(component_data.get("max_amount", 0))),
                    is_legendary=plan.is_legendary
                )
                
                self.db_session.add(component)
                
                # Calculate annual value
                annual_value = await self._calculate_annual_value(component)
                total_annual_value += annual_value
            
            plan.total_annual_value = total_annual_value
            
            # Create equity grants if specified
            if "equity" in plan_data:
                await self._create_equity_grants(user_id, plan_data["equity"])
            
            await self.db_session.commit()
            
            self.logger.info(f"Compensation plan created for {user_id} by {created_by}")
            
            # Special handling for legendary plans
            if plan.is_legendary:
                self.logger.info(f"🎸 LEGENDARY COMPENSATION PLAN created for {user_id}! Total: ${total_annual_value:,.2f} 🎸")
            
            return {
                "success": True,
                "plan_id": plan.plan_id,
                "total_annual_value": float(total_annual_value),
                "currency": plan.currency,
                "is_legendary": plan.is_legendary,
                "message": f"Compensation plan created with total value ${total_annual_value:,.2f}" + (" with LEGENDARY status!" if plan.is_legendary else ""),
                "legendary_perks": plan.is_legendary
            }
            
        except Exception as e:
            self.logger.error(f"Compensation plan creation failed: {e}")
            await self.db_session.rollback()
            return {"success": False, "error": str(e)}
    
    async def _validate_compensation_authority(self, approver_id: str, target_user_id: str) -> bool:
        """Validate authority to modify compensation"""
        
        # RICKROLL187 can modify anyone's compensation
        if approver_id == "rickroll187":
            return True
        
        # Check if approver has HR or executive permissions
        # This would integrate with your user management system
        allowed_roles = ["admin", "hr_director", "vp", "ceo", "legendary_founder"]
        
        # Mock authorization check - replace with actual role validation
        return True  # Placeholder for demo
    
    async def _calculate_annual_value(self, component: CompensationComponent) -> Decimal:
        """Calculate annual value of compensation component"""
        
        base_amount = component.base_amount
        
        # Convert to annual based on frequency
        multipliers = {
            PayFrequency.WEEKLY: 52,
            PayFrequency.BI_WEEKLY: 26,
            PayFrequency.MONTHLY: 12,
            PayFrequency.QUARTERLY: 4,
            PayFrequency.ANNUALLY: 1,
            PayFrequency.LEGENDARY_CONTINUOUS: 1  # Already annual for continuous
        }
        
        multiplier = multipliers.get(component.pay_frequency, 1)
        annual_value = base_amount * multiplier
        
        # Apply legendary multiplier if applicable
        if component.is_legendary:
            legendary_bonus = self.calculation_engines["salary_formula"]["base_multipliers"]["legendary_status"]
            annual_value *= (Decimal("1.0") + Decimal(str(legendary_bonus)))
        
        return annual_value
    
    async def _create_equity_grants(self, user_id: str, equity_data: List[Dict[str, Any]]):
        """Create equity grants for user"""
        
        for grant_data in equity_data:
            # Determine vesting schedule based on user level
            is_legendary = user_id == "rickroll187"
            vesting_schedule = "legendary" if is_legendary else grant_data.get("vesting_schedule", "standard")
            
            schedule_config = self.calculation_engines["equity_calculator"]["vesting_schedules"][vesting_schedule]
            
            grant = EquityGrant(
                user_id=user_id,
                equity_type=EquityType(grant_data["type"]),
                grant_date=datetime.strptime(grant_data["grant_date"], "%Y-%m-%d").date(),
                vesting_start_date=datetime.strptime(grant_data.get("vesting_start", grant_data["grant_date"]), "%Y-%m-%d").date(),
                vesting_cliff_months=schedule_config["cliff"],
                total_vesting_months=schedule_config["total"],
                total_shares=grant_data["shares"],
                strike_price=Decimal(str(grant_data.get("strike_price", "0.00"))),
                current_fair_value=self.equity_manager["current_409a_price"],
                is_legendary_grant=is_legendary
            )
            
            # Apply legendary strike price discount
            if is_legendary:
                discount = self.equity_manager["strike_price_discounts"]["legendary"]
                grant.strike_price *= (Decimal("1.0") - Decimal(str(discount)))
            
            self.db_session.add(grant)
    
    async def calculate_bonus(self, user_id: str, period_start: str, period_end: str, 
                           performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance-based bonus with legendary precision"""
        
        try:
            # Get user's bonus components
            bonus_components = self.db_session.query(CompensationComponent).join(CompensationPlan).filter(
                CompensationPlan.user_id == user_id,
                CompensationComponent.component_type == CompensationType.BONUS,
                CompensationPlan.status == CompensationStatus.ACTIVE
            ).all()
            
            if not bonus_components:
                return {"success": False, "error": "No active bonus components found"}
            
            total_bonus = Decimal("0.00")
            calculation_details = []
            
            for component in bonus_components:
                # Calculate base bonus amount
                if component.calculation_formula:
                    base_amount = await self._evaluate_bonus_formula(
                        component.calculation_formula, 
                        user_id, 
                        performance_data
                    )
                else:
                    base_amount = component.base_amount
                
                # Apply performance multiplier
                performance_score = Decimal(str(performance_data.get("overall_score", 3.0)))
                performance_multiplier = performance_score / Decimal("5.0")  # Normalize to 0-1
                
                # Calculate weighted performance score
                weights = self.calculation_engines["bonus_calculator"]["performance_weights"]
                weighted_score = (
                    Decimal(str(performance_data.get("individual_performance", 3.0) * weights["individual_performance"])) +
                    Decimal(str(performance_data.get("team_performance", 3.0) * weights["team_performance"])) +
                    Decimal(str(performance_data.get("company_performance", 3.0) * weights["company_performance"]))
                ) / Decimal("5.0")
                
                # Calculate final bonus
                calculated_bonus = base_amount * weighted_score
                
                # Apply min/max limits
                if component.minimum_amount:
                    calculated_bonus = max(calculated_bonus, component.minimum_amount)
                if component.maximum_amount:
                    calculated_bonus = min(calculated_bonus, component.maximum_amount)
                
                # Legendary bonus multiplier
                if component.is_legendary or user_id == "rickroll187":
                    legendary_multiplier = Decimal(str(self.calculation_engines["bonus_calculator"]["legendary_multiplier"]))
                    calculated_bonus *= legendary_multiplier
                    
                    # Swiss precision bonus
                    swiss_bonus = Decimal(str(self.calculation_engines["bonus_calculator"]["swiss_precision_bonus"]))
                    calculated_bonus *= (Decimal("1.0") + swiss_bonus)
                
                total_bonus += calculated_bonus
                
                calculation_details.append({
                    "component_name": component.component_name,
                    "base_amount": float(base_amount),
                    "performance_score": float(performance_score),
                    "weighted_score": float(weighted_score),
                    "calculated_amount": float(calculated_bonus),
                    "is_legendary": component.is_legendary
                })
            
            # Create bonus calculation record
            bonus_calculation = BonusCalculation(
                user_id=user_id,
                bonus_type=BonusType.PERFORMANCE_BASED,
                calculation_period_start=datetime.strptime(period_start, "%Y-%m-%d").date(),
                calculation_period_end=datetime.strptime(period_end, "%Y-%m-%d").date(),
                base_amount=sum(Decimal(str(detail["base_amount"])) for detail in calculation_details),
                performance_score=performance_score,
                performance_multiplier=weighted_score,
                calculated_amount=total_bonus,
                final_amount=total_bonus,
                is_legendary_bonus=user_id == "rickroll187"
            )
            
            self.db_session.add(bonus_calculation)
            await self.db_session.commit()
            
            self.logger.info(f"Bonus calculated for {user_id}: ${total_bonus:,.2f}")
            
            # Special logging for legendary bonuses
            if user_id == "rickroll187":
                self.logger.info(f"🎸 LEGENDARY BONUS calculated: ${total_bonus:,.2f} with Swiss precision! 🎸")
            
            return {
                "success": True,
                "calculation_id": bonus_calculation.calculation_id,
                "total_bonus": float(total_bonus),
                "calculation_details": calculation_details,
                "is_legendary_bonus": bonus_calculation.is_legendary_bonus,
                "performance_score": float(performance_score),
                "weighted_performance": float(weighted_score),
                "legendary_multipliers_applied": user_id == "rickroll187"
            }
            
        except Exception as e:
            self.logger.error(f"Bonus calculation failed: {e}")
            await self.db_session.rollback()
            return {"success": False, "error": str(e)}
    
    async def _evaluate_bonus_formula(self, formula: str, user_id: str, 
                                    performance_data: Dict[str, Any]) -> Decimal:
        """Safely evaluate bonus calculation formula"""
        
        try:
            # Get user's base salary for formula calculation
            base_salary = await self._get_user_base_salary(user_id)
            
            # Prepare safe variables for formula evaluation
            variables = {
                "base_salary": float(base_salary),
                "performance_score": performance_data.get("overall_score", 3.0),
                "individual_performance": performance_data.get("individual_performance", 3.0),
                "team_performance": performance_data.get("team_performance", 3.0),
                "company_performance": performance_data.get("company_performance", 3.0),
                "years_of_service": performance_data.get("years_of_service", 1),
                "department_multiplier": performance_data.get("department_multiplier", 1.0)
            }
            
            # Add legendary variables
            if user_id == "rickroll187":
                variables.update({
                    "legendary_status": True,
                    "swiss_precision_multiplier": 1.15,
                    "code_bro_bonus": 0.10
                })
            
            # Safe formula evaluation using ast.literal_eval for simple expressions
            # Replace variables in formula
            safe_formula = formula
            for var_name, var_value in variables.items():
                safe_formula = safe_formula.replace(f"{{{var_name}}}", str(var_value))
            
            # Basic mathematical operations only
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.USub: operator.neg,
                ast.UAdd: operator.pos,
            }
            
            # Parse and evaluate safely
            try:
                node = ast.parse(safe_formula, mode='eval')
                result = self._eval_ast_node(node.body, allowed_operators, variables)
                return Decimal(str(result))
            except:
                # Fallback to base calculation
                return Decimal(str(variables["base_salary"] * 0.10))  # 10% of base salary
                
        except Exception as e:
            self.logger.error(f"Formula evaluation failed: {e}")
            return Decimal("0.00")
    
    def _eval_ast_node(self, node, operators, variables):
        """Safely evaluate AST node"""
        
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            return variables.get(node.id, 0)
        elif isinstance(node, ast.BinOp):
            left = self._eval_ast_node(node.left, operators, variables)
            right = self._eval_ast_node(node.right, operators, variables)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_ast_node(node.operand, operators, variables)
            return operators[type(node.op)](operand)
        else:
            raise ValueError(f"Unsupported operation: {type(node)}")
    
    async def _get_user_base_salary(self, user_id: str) -> Decimal:
        """Get user's current base salary"""
        
        try:
            component = self.db_session.query(CompensationComponent).join(CompensationPlan).filter(
                CompensationPlan.user_id == user_id,
                CompensationComponent.component_type == CompensationType.BASE_SALARY,
                CompensationPlan.status == CompensationStatus.ACTIVE
            ).first()
            
            if component:
                return component.base_amount
            else:
                return Decimal("50000.00")  # Default base salary
                
        except Exception:
            return Decimal("50000.00")  # Fallback
    
    async def process_payroll(self, pay_period_start: str, pay_period_end: str, 
                            user_ids: List[str] = None) -> Dict[str, Any]:
        """Process payroll for specified period"""
        
        try:
            period_start = datetime.strptime(pay_period_start, "%Y-%m-%d").date()
            period_end = datetime.strptime(pay_period_end, "%Y-%m-%d").date()
            
            # Get users to process
            if user_ids:
                users_query = self.db_session.query(CompensationPlan).filter(
                    CompensationPlan.user_id.in_(user_ids),
                    CompensationPlan.status == CompensationStatus.ACTIVE
                )
            else:
                users_query = self.db_session.query(CompensationPlan).filter(
                    CompensationPlan.status == CompensationStatus.ACTIVE
                )
            
            compensation_plans = users_query.all()
            
            payroll_records = []
            total_gross_pay = Decimal("0.00")
            total_net_pay = Decimal("0.00")
            
            for plan in compensation_plans:
                payroll_record = await self._process_individual_payroll(plan, period_start, period_end)
                if payroll_record:
                    payroll_records.append(payroll_record)
                    total_gross_pay += payroll_record.gross_pay
                    total_net_pay += payroll_record.net_pay
            
            await self.db_session.commit()
            
            self.logger.info(f"Payroll processed for {len(payroll_records)} employees")
            
            # Count legendary payrolls
            legendary_count = len([r for r in payroll_records if r.is_legendary])
            if legendary_count > 0:
                self.logger.info(f"🎸 {legendary_count} LEGENDARY payroll(s) processed with Swiss precision! 🎸")
            
            return {
                "success": True,
                "pay_period_start": pay_period_start,
                "pay_period_end": pay_period_end,
                "total_employees": len(payroll_records),
                "legendary_employees": legendary_count,
                "total_gross_pay": float(total_gross_pay),
                "total_net_pay": float(total_net_pay),
                "payroll_records": [
                    {
                        "payroll_id": record.payroll_id,
                        "user_id": record.user_id,
                        "gross_pay": float(record.gross_pay),
                        "net_pay": float(record.net_pay),
                        "is_legendary": record.is_legendary
                    }
                    for record in payroll_records
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Payroll processing failed: {e}")
            await self.db_session.rollback()
            return {"success": False, "error": str(e)}
    
    async def _process_individual_payroll(self, plan: CompensationPlan, 
                                        period_start: datetime, period_end: datetime) -> Optional[PayrollSummary]:
        """Process payroll for individual employee"""
        
        try:
            user_id = plan.user_id
            is_legendary = plan.is_legendary or user_id == "rickroll187"
            
            # Calculate gross pay components
            base_pay = await self._calculate_base_pay(plan, period_start, period_end)
            overtime_pay = Decimal("0.00")  # Would integrate with time tracking
            bonus_pay = await self._calculate_period_bonus(user_id, period_start, period_end)
            commission_pay = await self._calculate_commission(user_id, period_start, period_end)
            
            gross_pay = base_pay + overtime_pay + bonus_pay + commission_pay
            
            # Calculate deductions
            deductions = await self._calculate_deductions(user_id, gross_pay, is_legendary)
            
            # Calculate taxes
            taxes = await self._calculate_taxes(user_id, gross_pay, period_start)
            
            # Calculate net pay
            total_deductions = sum(Decimal(str(d)) for d in deductions.values())
            total_taxes = sum(Decimal(str(t)) for t in taxes.values())
            net_pay = gross_pay - total_deductions - total_taxes
            
            # Create payroll record
            payroll_record = PayrollRecord(
                user_id=user_id,
                pay_period_start=period_start,
                pay_period_end=period_end,
                gross_pay=gross_pay,
                base_pay=base_pay,
                overtime_pay=overtime_pay,
                bonus_pay=bonus_pay,
                commission_pay=commission_pay,
                deductions=deductions,
                taxes=taxes,
                net_pay=net_pay,
                pay_date=period_end + timedelta(days=3),  # Pay 3 days after period end
                is_legendary_pay=is_legendary
            )
            
            self.db_session.add(payroll_record)
            
            return PayrollSummary(
                payroll_id=payroll_record.payroll_id,
                user_id=user_id,
                pay_period=f"{period_start} to {period_end}",
                gross_pay=gross_pay,
                net_pay=net_pay,
                deductions_total=total_deductions,
                taxes_total=total_taxes,
                is_legendary=is_legendary
            )
            
        except Exception as e:
            self.logger.error(f"Individual payroll processing failed for {plan.user_id}: {e}")
            return None
    
    async def _calculate_base_pay(self, plan: CompensationPlan, 
                                period_start: datetime, period_end: datetime) -> Decimal:
        """Calculate base pay for period"""
        
        # Get base salary component
        base_component = next((c for c in plan.components if c.component_type == CompensationType.BASE_SALARY), None)
        
        if not base_component:
            return Decimal("0.00")
        
        # Calculate period pay based on frequency
        days_in_period = (period_end - period_start).days + 1
        
        if base_component.pay_frequency == PayFrequency.ANNUALLY:
            daily_rate = base_component.base_amount / Decimal("365")
        elif base_component.pay_frequency == PayFrequency.MONTHLY:
            daily_rate = base_component.base_amount / Decimal("30")
        elif base_component.pay_frequency == PayFrequency.BI_WEEKLY:
            daily_rate = base_component.base_amount / Decimal("14")
        elif base_component.pay_frequency == PayFrequency.WEEKLY:
            daily_rate = base_component.base_amount / Decimal("7")
        else:
            daily_rate = base_component.base_amount / Decimal("365")  # Default to annual
        
        period_pay = daily_rate * Decimal(str(days_in_period))
        
        # Apply legendary continuous pay adjustment
        if base_component.pay_frequency == PayFrequency.LEGENDARY_CONTINUOUS:
            # Real-time pay calculation with Swiss precision
            period_pay *= Decimal("1.05")  # 5% continuous pay premium
        
        return period_pay
    
    async def _calculate_period_bonus(self, user_id: str, period_start: datetime, period_end: datetime) -> Decimal:
        """Calculate bonus pay for period"""
        
        # Get pending bonus calculations for this period
        bonus_calculations = self.db_session.query(BonusCalculation).filter(
            BonusCalculation.user_id == user_id,
            BonusCalculation.calculation_period_start >= period_start,
            BonusCalculation.calculation_period_end <= period_end,
            BonusCalculation.approval_status == "approved"
        ).all()
        
        total_bonus = sum(calc.final_amount for calc in bonus_calculations)
        return Decimal(str(total_bonus))
    
    async def _calculate_commission(self, user_id: str, period_start: datetime, period_end: datetime) -> Decimal:
        """Calculate commission pay for period"""
        
        # This would integrate with sales/revenue tracking
        # For now, return 0
        return Decimal("0.00")
    
    async def _calculate_deductions(self, user_id: str, gross_pay: Decimal, is_legendary: bool) -> Dict[str, float]:
        """Calculate payroll deductions"""
        
        deductions = {}
        benefits = self.benefits_integration
        
        # Health insurance
        health_cost = Decimal(str(benefits["health_insurance"]["annual_company_cost"]))
        employee_health_cost = health_cost * Decimal(str(benefits["health_insurance"]["employee_cost_percentage"]))
        deductions["health_insurance"] = float(employee_health_cost / Decimal("12"))  # Monthly
        
        # Dental insurance
        dental_cost = Decimal(str(benefits["dental_insurance"]["annual_company_cost"]))
        employee_dental_cost = dental_cost * Decimal(str(benefits["dental_insurance"]["employee_cost_percentage"]))
        deductions["dental_insurance"] = float(employee_dental_cost / Decimal("12"))  # Monthly
        
        # Vision insurance
        vision_cost = Decimal(str(benefits["vision_insurance"]["annual_company_cost"]))
        employee_vision_cost = vision_cost * Decimal(str(benefits["vision_insurance"]["employee_cost_percentage"]))
        deductions["vision_insurance"] = float(employee_vision_cost / Decimal("12"))  # Monthly
        
        # 401k contribution (assume 6% employee contribution)
        retirement_contribution = gross_pay * Decimal("0.06")
        deductions["retirement_401k"] = float(retirement_contribution)
        
        # Legendary users get premium deductions waived
        if is_legendary:
            deductions["health_insurance"] = 0.0
            deductions["dental_insurance"] = 0.0
            deductions["vision_insurance"] = 0.0
            deductions["legendary_premium_waiver"] = -500.0  # Credit
        
        return deductions
    
    async def _calculate_taxes(self, user_id: str, gross_pay: Decimal, period_start: datetime) -> Dict[str, float]:
        """Calculate tax withholdings"""
        
        taxes = {}
        tax_engine = self.tax_engine
        
        # Calculate annual gross for tax brackets
        annual_gross = gross_pay * Decimal("12")  # Assume monthly pay
        
        # Federal income tax (simplified)
        federal_tax = self._calculate_federal_tax(annual_gross) / Decimal("12")
        taxes["federal_income"] = float(federal_tax)
        
        # State tax (assume California for example)
        state_rate = Decimal(str(tax_engine["state_tax_rates"]["CA"]))
        state_tax = gross_pay * state_rate
        taxes["state_income"] = float(state_tax)
        
        # Payroll taxes
        social_security = gross_pay * Decimal(str(tax_engine["payroll_taxes"]["social_security"]))
        medicare = gross_pay * Decimal(str(tax_engine["payroll_taxes"]["medicare"]))
        
        taxes["social_security"] = float(social_security)
        taxes["medicare"] = float(medicare)
        
        # Legendary tax optimization
        if user_id == "rickroll187" and tax_engine["legendary_tax_optimization"]:
            # Apply legendary tax strategies (legal optimization)
            total_tax = sum(taxes.values())
            optimization_savings = total_tax * 0.15  # 15% savings through optimization
            taxes["legendary_tax_optimization"] = -optimization_savings
        
        return taxes
    
    def _calculate_federal_tax(self, annual_income: Decimal) -> Decimal:
        """Calculate federal income tax using brackets"""
        
        brackets = self.tax_engine["federal_tax_brackets"]
        total_tax = Decimal("0.00")
        remaining_income = annual_income
        
        for bracket in brackets:
            bracket_min = Decimal(str(bracket["min"]))
            bracket_max = Decimal(str(bracket["max"]))
            bracket_rate = Decimal(str(bracket["rate"]))
            
            if remaining_income <= Decimal("0"):
                break
            
            if annual_income > bracket_min:
                taxable_in_bracket = min(remaining_income, bracket_max - bracket_min)
                tax_in_bracket = taxable_in_bracket * bracket_rate
                total_tax += tax_in_bracket
                remaining_income -= taxable_in_bracket
        
        return total_tax
    
    async def get_compensation_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive compensation summary"""
        
        try:
            # Get active compensation plan
            plan = self.db_session.query(CompensationPlan).filter(
                CompensationPlan.user_id == user_id,
                CompensationPlan.status == CompensationStatus.ACTIVE
            ).first()
            
            if not plan:
                return {"success": False, "error": "No active compensation plan found"}
            
            # Calculate component values
            base_salary = Decimal("0.00")
            variable_pay = Decimal("0.00")
            
            for component in plan.components:
                annual_value = await self._calculate_annual_value(component)
                
                if component.component_type == CompensationType.BASE_SALARY:
                    base_salary += annual_value
                elif component.component_type in [CompensationType.BONUS, CompensationType.COMMISSION]:
                    variable_pay += annual_value
            
            # Calculate equity value
            equity_value = await self._calculate_equity_value(user_id)
            
            # Calculate benefits value
            benefits_value = await self._calculate_benefits_value(user_id)
            
            # Total compensation
            total_compensation = base_salary + variable_pay + equity_value + benefits_value
            
            # Get recent payroll
            recent_payroll = self.db_session.query(PayrollRecord).filter(
                PayrollRecord.user_id == user_id
            ).order_by(PayrollRecord.created_at.desc()).limit(3).all()
            
            # Get equity grants
            equity_grants = self.db_session.query(EquityGrant).filter(
                EquityGrant.user_id == user_id
            ).all()
            
            summary = CompensationSummary(
                user_id=user_id,
                base_salary=base_salary,
                variable_pay=variable_pay,
                equity_value=equity_value,
                benefits_value=benefits_value,
                total_compensation=total_compensation,
                currency=plan.currency,
                is_legendary=plan.is_legendary
            )
            
            return {
                "success": True,
                "compensation_summary": {
                    "user_id": summary.user_id,
                    "base_salary": float(summary.base_salary),
                    "variable_pay": float(summary.variable_pay),
                    "equity_value": float(summary.equity_value),
                    "benefits_value": float(summary.benefits_value),
                    "total_compensation": float(summary.total_compensation),
                    "currency": summary.currency,
                    "is_legendary": summary.is_legendary
                },
                "plan_details": {
                    "plan_id": plan.plan_id,
                    "plan_name": plan.plan_name,
                    "effective_date": plan.effective_date.isoformat(),
                    "status": plan.status.value,
                    "components_count": len(plan.components)
                },
                "recent_payroll": [
                    {
                        "payroll_id": payroll.payroll_id,
                        "pay_period": f"{payroll.pay_period_start} to {payroll.pay_period_end}",
                        "gross_pay": float(payroll.gross_pay),
                        "net_pay": float(payroll.net_pay),
                        "is_legendary": payroll.is_legendary_pay
                    }
                    for payroll in recent_payroll
                ],
                "equity_grants": [
                    {
                        "grant_id": grant.grant_id,
                        "equity_type": grant.equity_type.value,
                        "total_shares": grant.total_shares,
                        "vested_shares": grant.vested_shares,
                        "current_value": float(grant.current_fair_value * grant.vested_shares),
                        "is_legendary": grant.is_legendary_grant
                    }
                    for grant in equity_grants
                ],
                "legendary_status": {
                    "is_legendary_user": plan.is_legendary,
                    "legendary_perks": plan.is_legendary,
                    "swiss_precision_compensation": True,
                    "legendary_message": "🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸" if plan.is_legendary else None
                }
            }
            
        except Exception as e:
            self.logger.error(f"Compensation summary generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _calculate_equity_value(self, user_id: str) -> Decimal:
        """Calculate current equity value"""
        
        equity_grants = self.db_session.query(EquityGrant).filter(
            EquityGrant.user_id == user_id
        ).all()
        
        total_value = Decimal("0.00")
        current_price = self.equity_manager["current_409a_price"]
        
        for grant in equity_grants:
            # Calculate vested shares
            vested_shares = await self._calculate_vested_shares(grant)
            grant.vested_shares = vested_shares
            
            # Calculate value
            if grant.equity_type == EquityType.STOCK_OPTIONS:
                # Option value is current price minus strike price
                option_value = max(Decimal("0"), current_price - grant.strike_price)
                total_value += option_value * vested_shares
            else:
                # RSU/other equity at current fair value
                total_value += current_price * vested_shares
        
        return total_value
    
    async def _calculate_vested_shares(self, grant: EquityGrant) -> int:
        """Calculate number of vested shares"""
        
        today = datetime.now().date()
        vesting_start = grant.vesting_start_date
        
        # Check if cliff period has passed
        cliff_date = vesting_start + timedelta(days=grant.vesting_cliff_months * 30)
        if today < cliff_date:
            return 0
        
        # Calculate vesting progress
        total_vesting_days = grant.total_vesting_months * 30
        days_since_start = (today - vesting_start).days
        
        if days_since_start >= total_vesting_days:
            # Fully vested
            return grant.total_shares
        
        # Linear vesting after cliff
        vesting_percentage = days_since_start / total_vesting_days
        vested_shares = int(grant.total_shares * vesting_percentage)
        
        # Legendary grants get acceleration
        if grant.is_legendary_grant:
            acceleration_factor = 1.25  # 25% faster vesting
            vested_shares = min(int(vested_shares * acceleration_factor), grant.total_shares)
        
        return vested_shares
    
    async def _calculate_benefits_value(self, user_id: str) -> Decimal:
        """Calculate annual benefits value"""
        
        benefits = self.benefits_integration
        total_value = Decimal("0.00")
        
        # Health insurance company contribution
        health_value = Decimal(str(benefits["health_insurance"]["annual_company_cost"]))
        health_company_portion = health_value * Decimal(str(benefits["health_insurance"]["company_cost_percentage"]))
        total_value += health_company_portion
        
        # Other insurance
        total_value += Decimal(str(benefits["dental_insurance"]["annual_company_cost"]))
        total_value += Decimal(str(benefits["vision_insurance"]["annual_company_cost"]))
        
        # 401k match (assume 4% match on $100k salary)
        retirement_match = Decimal("4000.00")  # Would calculate based on actual salary
        total_value += retirement_match
        
        # PTO value (assume $400/day for 25 days)
        pto_value = Decimal("10000.00")
        total_value += pto_value
        
        # Legendary perks
        if user_id == "rickroll187":
            legendary_perks = benefits["legendary_perks"]
            total_value += Decimal(str(legendary_perks["swiss_precision_bonus"]))
            total_value += Decimal(str(legendary_perks["code_bro_events_budget"]))
            total_value += Decimal(str(legendary_perks["legendary_workspace_allowance"]))
            total_value += Decimal(str(legendary_perks["professional_development"]))
            total_value += Decimal(str(legendary_perks["wellness_stipend"]))
        
        return total_value

# Global compensation system instance
legendary_compensation_system = None

def get_legendary_compensation_system(db_session: Session) -> LegendaryCompensationSystem:
    """Get legendary compensation system instance"""
    global legendary_compensation_system
    if legendary_compensation_system is None:
        legendary_compensation_system = LegendaryCompensationSystem(db_session)
    return legendary_compensation_system
