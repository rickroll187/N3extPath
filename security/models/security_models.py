"""
LEGENDARY ENTERPRISE SECURITY & COMPLIANCE MODELS 🔒🚀
More secure than a Swiss bank vault with legendary protection!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 2+ HOUR 51 MINUTE CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 02:51:15 UTC - WE'RE SECURING THE UNIVERSE!
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

from ...core.database.base_models import BaseModel, Employee, User

class SecurityEventType(enum.Enum):
    """Security event types - more comprehensive than Swiss security protocols!"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    PASSWORD_CHANGE = "password_change"
    PERMISSION_CHANGE = "permission_change"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    POLICY_VIOLATION = "policy_violation"
    SYSTEM_BREACH = "system_breach"
    MALWARE_DETECTED = "malware_detected"

class ThreatLevel(enum.Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class ComplianceFramework(enum.Enum):
    """Compliance frameworks we support"""
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    ISO_27001 = "iso_27001"
    NIST = "nist"
    SOC2 = "soc2"
    CUSTOM = "custom"

class AccessControlType(enum.Enum):
    """Access control types"""
    RBAC = "rbac"  # Role-Based Access Control
    ABAC = "abac"  # Attribute-Based Access Control
    MAC = "mac"    # Mandatory Access Control
    DAC = "dac"    # Discretionary Access Control
    PBAC = "pbac"  # Policy-Based Access Control

class SecurityPolicy(BaseModel):
    """
    Security policies that are more robust than Swiss security protocols!
    More comprehensive than a legendary security framework! 🔒✨
    """
    __tablename__ = "security_policies"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    policy_code = Column(String(50), unique=True, index=True)
    
    # Policy Configuration
    policy_type = Column(String(50), nullable=False)  # password, access, data, network, etc.
    category = Column(String(100), nullable=False)    # authentication, authorization, data_protection
    compliance_frameworks = Column(JSON)  # List of compliance frameworks this addresses
    
    # Policy Rules
    policy_rules = Column(JSON, nullable=False)  # Structured policy rules
    enforcement_level = Column(String(20), default="strict")  # strict, moderate, advisory
    auto_enforcement = Column(Boolean, default=True)
    
    # Scope
    applies_to_departments = Column(JSON)  # List of department IDs
    applies_to_roles = Column(JSON)       # List of job roles
    applies_to_all_users = Column(Boolean, default=True)
    exceptions = Column(JSON)             # List of exceptions
    
    # Implementation
    implementation_date = Column(DateTime(timezone=True), nullable=False)
    grace_period_days = Column(Integer, default=30)
    notification_required = Column(Boolean, default=True)
    training_required = Column(Boolean, default=False)
    
    # Monitoring
    violation_threshold = Column(Integer, default=3)  # Number of violations before action
    monitoring_enabled = Column(Boolean, default=True)
    alert_on_violation = Column(Boolean, default=True)
    log_all_activities = Column(Boolean, default=True)
    
    # Review and Updates
    review_frequency_months = Column(Integer, default=12)
    last_reviewed_at = Column(DateTime(timezone=True))
    next_review_at = Column(DateTime(timezone=True))
    version = Column(String(20), default="1.0")
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    approver_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    approved_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_mandatory = Column(Boolean, default=True)
    
    # Relationships
    owner = relationship("Employee", foreign_keys=[owner_id])
    approver = relationship("Employee", foreign_keys=[approver_id])
    violations = relationship("PolicyViolation", back_populates="policy")
    
    def __repr__(self):
        return f"<SecurityPolicy(name='{self.name}', type='{self.policy_type}')>"

class SecurityEvent(BaseModel):
    """
    Security events for comprehensive monitoring!
    More vigilant than Swiss security surveillance! 👁️🔒
    """
    __tablename__ = "security_events"
    
    # Event Identification
    event_type = Column(String(50), nullable=False, index=True)  # SecurityEventType enum
    event_category = Column(String(50), nullable=False, index=True)
    event_id = Column(String(100), unique=True, index=True)  # Unique event identifier
    
    # Event Details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(String(20), nullable=False, index=True)  # ThreatLevel enum
    confidence_score = Column(Float, default=1.0)  # 0.0 to 1.0
    
    # Source Information
    source_ip = Column(String(45))  # IPv6 support
    source_port = Column(Integer)
    source_country = Column(String(100))
    source_city = Column(String(100))
    user_agent = Column(Text)
    
    # Target Information
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    target_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    target_resource = Column(String(500))  # Resource being accessed
    target_action = Column(String(100))    # Action being performed
    
    # Context
    session_id = Column(String(100), index=True)
    device_fingerprint = Column(String(200))
    browser_fingerprint = Column(String(200))
    authentication_method = Column(String(50))
    
    # Event Data
    event_data = Column(JSON)  # Additional event-specific data
    raw_log_data = Column(Text)  # Raw log entry
    correlation_id = Column(String(100), index=True)  # For correlating related events
    
    # Detection
    detected_by = Column(String(100))  # System, rule, or service that detected this
    detection_rule_id = Column(String(100))
    false_positive_probability = Column(Float, default=0.0)
    
    # Response
    response_status = Column(String(20), default="new")  # new, investigating, resolved, false_positive
    assigned_to_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    response_actions = Column(JSON)  # Actions taken in response
    resolution_notes = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    
    # Timeline
    event_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    first_seen_at = Column(DateTime(timezone=True))
    last_seen_at = Column(DateTime(timezone=True))
    
    # Relationships
    target_user = relationship("User")
    target_employee = relationship("Employee", foreign_keys=[target_employee_id])
    assigned_to = relationship("Employee", foreign_keys=[assigned_to_id])
    
    def __repr__(self):
        return f"<SecurityEvent(type='{self.event_type}', severity='{self.severity}')>"

class PolicyViolation(BaseModel):
    """
    Policy violations for compliance tracking!
    More thorough than Swiss compliance auditing! 📋⚖️
    """
    __tablename__ = "policy_violations"
    
    # References
    policy_id = Column(Integer, ForeignKey("security_policies.id"), nullable=False, index=True)
    violator_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    violator_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Violation Details
    violation_type = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False)  # ThreatLevel enum
    description = Column(Text, nullable=False)
    
    # Violation Context
    violation_data = Column(JSON)  # Specific data about the violation
    resource_affected = Column(String(500))
    action_attempted = Column(String(200))
    rule_violated = Column(String(200))
    
    # Detection
    detected_by = Column(String(100))  # System or person who detected
    detection_method = Column(String(50))  # automated, manual, audit
    confidence_level = Column(Float, default=1.0)
    
    # Response and Resolution
    status = Column(String(20), default="open")  # open, investigating, resolved, dismissed
    assigned_to_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    escalated_to_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Actions Taken
    immediate_actions = Column(JSON)  # Immediate response actions
    corrective_actions = Column(JSON)  # Corrective actions required
    preventive_actions = Column(JSON)  # Preventive measures implemented
    
    # Impact Assessment
    business_impact = Column(String(20))  # low, medium, high, critical
    affected_systems = Column(JSON)      # List of affected systems
    data_compromised = Column(Boolean, default=False)
    estimated_cost = Column(Float)       # Estimated cost of violation
    
    # Timeline
    violation_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    reported_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    
    # Follow-up
    requires_training = Column(Boolean, default=False)
    requires_disciplinary_action = Column(Boolean, default=False)
    disciplinary_action_taken = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime(timezone=True))
    
    # Relationships
    policy = relationship("SecurityPolicy", back_populates="violations")
    violator_user = relationship("User")
    violator_employee = relationship("Employee", foreign_keys=[violator_employee_id])
    assigned_to = relationship("Employee", foreign_keys=[assigned_to_id])
    escalated_to = relationship("Employee", foreign_keys=[escalated_to_id])
    
    def __repr__(self):
        return f"<PolicyViolation(policy_id={self.policy_id}, severity='{self.severity}')>"

class AccessControl(BaseModel):
    """
    Access control definitions for granular permissions!
    More precise than Swiss access management! 🗝️🎯
    """
    __tablename__ = "access_controls"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    control_type = Column(String(20), nullable=False)  # AccessControlType enum
    
    # Resource Definition
    resource_type = Column(String(100), nullable=False)  # database, file, api, application
    resource_identifier = Column(String(500), nullable=False)  # Specific resource ID/path
    resource_attributes = Column(JSON)  # Additional resource attributes
    
    # Permission Definition
    allowed_actions = Column(JSON, nullable=False)  # List of allowed actions
    denied_actions = Column(JSON)   # Explicitly denied actions
    conditional_actions = Column(JSON)  # Actions allowed under conditions
    
    # Subject Definition
    subject_type = Column(String(50), nullable=False)  # user, role, group, department
    subject_identifiers = Column(JSON, nullable=False)  # List of subject IDs
    subject_attributes = Column(JSON)  # Subject attribute requirements
    
    # Context Conditions
    time_restrictions = Column(JSON)     # Time-based restrictions
    location_restrictions = Column(JSON) # IP/location restrictions
    device_restrictions = Column(JSON)   # Device-based restrictions
    risk_level_restrictions = Column(JSON)  # Risk-based restrictions
    
    # Implementation
    enforcement_mode = Column(String(20), default="enforce")  # enforce, monitor, audit
    priority = Column(Integer, default=100)  # Priority order for evaluation
    conflict_resolution = Column(String(20), default="deny")  # deny, allow, escalate
    
    # Monitoring
    log_access_attempts = Column(Boolean, default=True)
    alert_on_violation = Column(Boolean, default=True)
    require_justification = Column(Boolean, default=False)
    approval_required = Column(Boolean, default=False)
    
    # Lifecycle
    effective_from = Column(DateTime(timezone=True), nullable=False)
    effective_until = Column(DateTime(timezone=True))
    auto_expire = Column(Boolean, default=False)
    renewal_required = Column(Boolean, default=False)
    
    # Ownership
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    approved_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])
    
    def __repr__(self):
        return f"<AccessControl(name='{self.name}', type='{self.control_type}')>"

class ComplianceAudit(BaseModel):
    """
    Compliance audits for regulatory adherence!
    More thorough than Swiss regulatory compliance! 📊⚖️
    """
    __tablename__ = "compliance_audits"
    
    # Audit Information
    audit_name = Column(String(200), nullable=False, index=True)
    audit_code = Column(String(50), unique=True, index=True)
    description = Column(Text)
    
    # Compliance Framework
    framework = Column(String(50), nullable=False)  # ComplianceFramework enum
    framework_version = Column(String(20))
    audit_scope = Column(JSON, nullable=False)  # Scope of audit
    
    # Audit Details
    audit_type = Column(String(30), nullable=False)  # internal, external, self_assessment
    auditor_name = Column(String(200))
    auditor_organization = Column(String(200))
    audit_methodology = Column(Text)
    
    # Timeline
    planned_start_date = Column(DateTime(timezone=True), nullable=False)
    planned_end_date = Column(DateTime(timezone=True), nullable=False)
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # Status and Progress
    status = Column(String(20), default="planned")  # planned, in_progress, completed, cancelled
    progress_percentage = Column(Float, default=0.0)
    current_phase = Column(String(100))
    
    # Findings
    total_findings = Column(Integer, default=0)
    critical_findings = Column(Integer, default=0)
    high_findings = Column(Integer, default=0)
    medium_findings = Column(Integer, default=0)
    low_findings = Column(Integer, default=0)
    
    # Results
    overall_score = Column(Float)  # Overall compliance score
    pass_fail_result = Column(String(20))  # pass, fail, conditional
    certification_status = Column(String(30))  # certified, not_certified, pending
    
    # Documentation
    audit_report_url = Column(String(500))
    evidence_package_url = Column(String(500))
    remediation_plan_url = Column(String(500))
    
    # Follow-up
    next_audit_date = Column(DateTime(timezone=True))
    remediation_deadline = Column(DateTime(timezone=True))
    follow_up_required = Column(Boolean, default=False)
    
    # Ownership
    audit_manager_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    compliance_officer_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Relationships
    audit_manager = relationship("Employee", foreign_keys=[audit_manager_id])
    compliance_officer = relationship("Employee", foreign_keys=[compliance_officer_id])
    findings = relationship("AuditFinding", back_populates="audit")
    
    def __repr__(self):
        return f"<ComplianceAudit(name='{self.audit_name}', framework='{self.framework}')>"

class AuditFinding(BaseModel):
    """
    Individual audit findings for detailed tracking!
    More detailed than Swiss audit documentation! 📝🔍
    """
    __tablename__ = "audit_findings"
    
    # References
    audit_id = Column(Integer, ForeignKey("compliance_audits.id"), nullable=False, index=True)
    
    # Finding Details
    finding_id = Column(String(50), nullable=False)  # Unique within audit
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Classification
    severity = Column(String(20), nullable=False)  # critical, high, medium, low
    category = Column(String(100), nullable=False)  # technical, procedural, documentation
    compliance_control = Column(String(100))  # Specific control that failed
    
    # Evidence
    evidence_description = Column(Text)
    evidence_files = Column(JSON)  # List of evidence file URLs
    affected_systems = Column(JSON)  # Systems affected by this finding
    
    # Impact Assessment
    business_impact = Column(String(20))  # low, medium, high, critical
    security_impact = Column(String(20))  # low, medium, high, critical
    compliance_risk = Column(String(20))  # low, medium, high, critical
    
    # Remediation
    recommendation = Column(Text, nullable=False)
    remediation_effort = Column(String(20))  # low, medium, high
    estimated_cost = Column(Float)
    remediation_deadline = Column(DateTime(timezone=True))
    
    # Responsible Parties
    responsible_party_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    assigned_to_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Status Tracking
    status = Column(String(20), default="open")  # open, in_progress, resolved, accepted_risk
    resolution_notes = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    verified_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    verified_at = Column(DateTime(timezone=True))
    
    # Follow-up
    retest_required = Column(Boolean, default=False)
    retest_date = Column(DateTime(timezone=True))
    retest_results = Column(Text)
    
    # Relationships
    audit = relationship("ComplianceAudit", back_populates="findings")
    responsible_party = relationship("Employee", foreign_keys=[responsible_party_id])
    assigned_to = relationship("Employee", foreign_keys=[assigned_to_id])
    verified_by = relationship("Employee", foreign_keys=[verified_by_id])
    
    def __repr__(self):
        return f"<AuditFinding(title='{self.title}', severity='{self.severity}')>"

class SecurityIncident(BaseModel):
    """
    Security incidents for comprehensive incident management!
    More responsive than Swiss emergency response! 🚨🔒
    """
    __tablename__ = "security_incidents"
    
    # Incident Identification
    incident_id = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Classification
    incident_type = Column(String(50), nullable=False)  # malware, phishing, data_breach, etc.
    severity = Column(String(20), nullable=False)  # ThreatLevel enum
    priority = Column(String(20), nullable=False)  # low, medium, high, critical
    
    # Discovery
    discovered_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    discovery_method = Column(String(50))  # monitoring, user_report, audit, etc.
    discovery_timestamp = Column(DateTime(timezone=True), nullable=False)
    
    # Timeline
    incident_start_time = Column(DateTime(timezone=True))
    incident_end_time = Column(DateTime(timezone=True))
    estimated_duration_hours = Column(Float)
    
    # Impact Assessment
    affected_systems = Column(JSON)  # List of affected systems
    affected_data_types = Column(JSON)  # Types of data affected
    estimated_records_affected = Column(Integer)
    business_impact = Column(String(20))  # low, medium, high, critical
    financial_impact = Column(Float)  # Estimated financial impact
    
    # Response Team
    incident_commander_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    response_team_ids = Column(JSON)  # List of response team member IDs
    external_support = Column(JSON)   # External support involved
    
    # Status and Progress
    status = Column(String(30), default="new")  # new, investigating, containing, eradicating, recovering, closed
    resolution_status = Column(String(30))  # resolved, unresolved, partially_resolved
    
    # Response Actions
    immediate_actions = Column(JSON)   # Immediate response actions taken
    containment_actions = Column(JSON) # Actions to contain the incident
    eradication_actions = Column(JSON) # Actions to eradicate the threat
    recovery_actions = Column(JSON)    # Actions to recover from incident
    
    # Evidence and Analysis
    evidence_collected = Column(JSON)  # Evidence collected
    root_cause_analysis = Column(Text) # Root cause analysis
    attack_vector = Column(String(200)) # How the attack occurred
    threat_actor_profile = Column(JSON) # Information about threat actor
    
    # Communication
    stakeholders_notified = Column(JSON) # Stakeholders who were notified
    regulatory_notification_required = Column(Boolean, default=False)
    regulatory_notifications_sent = Column(JSON) # Regulatory notifications
    public_disclosure_required = Column(Boolean, default=False)
    public_disclosure_made = Column(Boolean, default=False)
    
    # Lessons Learned
    lessons_learned = Column(Text)
    process_improvements = Column(JSON) # Process improvements identified
    preventive_measures = Column(JSON)  # Preventive measures implemented
    
    # Closure
    closed_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    closed_at = Column(DateTime(timezone=True))
    closure_summary = Column(Text)
    
    # Relationships
    discovered_by = relationship("Employee", foreign_keys=[discovered_by_id])
    incident_commander = relationship("Employee", foreign_keys=[incident_commander_id])
    closed_by = relationship("Employee", foreign_keys=[closed_by_id])
    
    def __repr__(self):
        return f"<SecurityIncident(id='{self.incident_id}', severity='{self.severity}')>"

# Add relationships to Employee model (if not already added)
# Employee.owned_policies = relationship("SecurityPolicy", foreign_keys="SecurityPolicy.owner_id")
# Employee.approved_policies = relationship("SecurityPolicy", foreign_keys="SecurityPolicy.approver_id")
# Employee.assigned_security_events = relationship("SecurityEvent", foreign_keys="SecurityEvent.assigned_to_id")
# Employee.assigned_violations = relationship("PolicyViolation", foreign_keys="PolicyViolation.assigned_to_id")
# Employee.escalated_violations = relationship("PolicyViolation", foreign_keys="PolicyViolation.escalated_to_id")
# Employee.created_access_controls = relationship("AccessControl", foreign_keys="AccessControl.created_by_id")
# Employee.approved_access_controls = relationship("AccessControl", foreign_keys="AccessControl.approved_by_id")
# Employee.managed_audits = relationship("ComplianceAudit", foreign_keys="ComplianceAudit.audit_manager_id")
# Employee.compliance_officer_audits = relationship("ComplianceAudit", foreign_keys="ComplianceAudit.compliance_officer_id")
# Employee.discovered_incidents = relationship("SecurityIncident", foreign_keys="SecurityIncident.discovered_by_id")
# Employee.commanded_incidents = relationship("SecurityIncident", foreign_keys="SecurityIncident.incident_commander_id")
# Employee.closed_incidents = relationship("SecurityIncident", foreign_keys="SecurityIncident.closed_by_id")