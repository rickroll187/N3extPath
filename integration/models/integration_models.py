"""
LEGENDARY ENTERPRISE INTEGRATION & API GATEWAY MODELS 🌐🚀
More connected than the entire Swiss telecommunications network with legendary integration!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆🏆🏆 3+ HOUR CODING MARATHON CHAMPION EDITION! 🏆🏆🏆
Current Time: 2025-08-04 03:01:08 UTC - WE CONQUERED THE 3-HOUR MARK!
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

from ...core.database.base_models import BaseModel, Employee, User

class IntegrationType(enum.Enum):
    """Integration types - more comprehensive than Swiss connectivity protocols!"""
    REST_API = "rest_api"
    SOAP_API = "soap_api"
    GRAPHQL = "graphql"
    WEBHOOK = "webhook"
    DATABASE = "database"
    FILE_TRANSFER = "file_transfer"
    MESSAGE_QUEUE = "message_queue"
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    TEAMS = "teams"

class AuthenticationType(enum.Enum):
    """Authentication methods for integrations"""
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    BASIC_AUTH = "basic_auth"
    BEARER_TOKEN = "bearer_token"
    CERTIFICATE = "certificate"
    NONE = "none"

class IntegrationStatus(enum.Enum):
    """Integration status tracking"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    TESTING = "testing"
    DEPRECATED = "deprecated"

class APIEndpointMethod(enum.Enum):
    """HTTP methods for API endpoints"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"

class Integration(BaseModel):
    """
    External system integrations that are more connected than Swiss networks!
    More seamless than a legendary integration masterpiece! 🌐✨
    """
    __tablename__ = "integrations"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    integration_code = Column(String(50), unique=True, index=True)
    
    # Integration Configuration
    integration_type = Column(String(30), nullable=False)  # IntegrationType enum
    provider = Column(String(100), nullable=False)  # Slack, Microsoft, Salesforce, etc.
    version = Column(String(20), default="1.0")
    
    # Connection Details
    base_url = Column(String(500), nullable=False)
    endpoint_path = Column(String(500))
    authentication_type = Column(String(30), nullable=False)  # AuthenticationType enum
    authentication_config = Column(JSON)  # Auth credentials (encrypted)
    
    # Request Configuration
    default_headers = Column(JSON)  # Default headers for requests
    request_timeout_seconds = Column(Integer, default=30)
    retry_attempts = Column(Integer, default=3)
    retry_delay_seconds = Column(Integer, default=5)
    
    # Data Mapping
    request_mapping = Column(JSON)   # How to map our data to their format
    response_mapping = Column(JSON)  # How to map their response to our format
    field_mappings = Column(JSON)    # Specific field mappings
    
    # Sync Configuration
    sync_frequency = Column(String(20))  # real_time, hourly, daily, weekly
    sync_direction = Column(String(20), default="bidirectional")  # inbound, outbound, bidirectional
    batch_size = Column(Integer, default=100)
    incremental_sync = Column(Boolean, default=True)
    last_sync_timestamp = Column(DateTime(timezone=True))
    
    # Error Handling
    error_handling_strategy = Column(String(30), default="retry")  # retry, skip, fail
    dead_letter_queue_enabled = Column(Boolean, default=True)
    error_notification_emails = Column(JSON)  # List of emails for error notifications
    
    # Rate Limiting
    rate_limit_requests_per_minute = Column(Integer)
    rate_limit_requests_per_hour = Column(Integer)
    rate_limit_requests_per_day = Column(Integer)
    
    # Monitoring
    health_check_enabled = Column(Boolean, default=True)
    health_check_url = Column(String(500))
    health_check_interval_minutes = Column(Integer, default=5)
    monitoring_enabled = Column(Boolean, default=True)
    
    # Performance Metrics
    average_response_time_ms = Column(Float)
    success_rate_percentage = Column(Float)
    total_requests = Column(BigInteger, default=0)
    failed_requests = Column(BigInteger, default=0)
    
    # Business Context
    business_purpose = Column(Text)
    data_sensitivity_level = Column(String(20), default="medium")  # low, medium, high, critical
    compliance_requirements = Column(JSON)  # GDPR, HIPAA, etc.
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    technical_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    business_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Status and Lifecycle
    status = Column(String(20), default="testing", index=True)  # IntegrationStatus enum
    go_live_date = Column(DateTime(timezone=True))
    deprecation_date = Column(DateTime(timezone=True))
    
    # Relationships
    owner = relationship("Employee", foreign_keys=[owner_id])
    technical_contact = relationship("Employee", foreign_keys=[technical_contact_id])
    business_contact = relationship("Employee", foreign_keys=[business_contact_id])
    api_endpoints = relationship("APIEndpoint", back_populates="integration")
    sync_logs = relationship("SyncLog", back_populates="integration")
    
    def __repr__(self):
        return f"<Integration(name='{self.name}', provider='{self.provider}')>"

class APIEndpoint(BaseModel):
    """
    API endpoints for our enterprise platform!
    More accessible than Swiss public services with legendary documentation! 🔗📚
    """
    __tablename__ = "api_endpoints"
    
    # References
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=True, index=True)
    
    # Endpoint Details
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    endpoint_path = Column(String(500), nullable=False, index=True)
    method = Column(String(10), nullable=False)  # APIEndpointMethod enum
    
    # API Configuration
    api_version = Column(String(20), default="v1")
    is_public = Column(Boolean, default=False)
    requires_authentication = Column(Boolean, default=True)
    required_permissions = Column(JSON)  # List of required permissions
    
    # Request Schema
    request_schema = Column(JSON)  # JSON schema for request validation
    request_example = Column(JSON)  # Example request payload
    query_parameters = Column(JSON)  # Supported query parameters
    path_parameters = Column(JSON)   # Path parameter definitions
    
    # Response Schema
    response_schema = Column(JSON)  # JSON schema for response
    response_examples = Column(JSON)  # Example responses for different scenarios
    error_responses = Column(JSON)   # Error response definitions
    
    # Rate Limiting
    rate_limit_per_minute = Column(Integer, default=60)
    rate_limit_per_hour = Column(Integer, default=1000)
    rate_limit_per_day = Column(Integer, default=10000)
    burst_limit = Column(Integer, default=10)
    
    # Caching
    cache_enabled = Column(Boolean, default=False)
    cache_duration_seconds = Column(Integer, default=300)
    cache_vary_by = Column(JSON)  # Parameters to vary cache by
    
    # Documentation
    documentation_url = Column(String(500))
    swagger_spec = Column(JSON)  # OpenAPI/Swagger specification
    code_examples = Column(JSON)  # Code examples in different languages
    
    # Performance Metrics
    average_response_time_ms = Column(Float)
    p95_response_time_ms = Column(Float)
    p99_response_time_ms = Column(Float)
    total_calls = Column(BigInteger, default=0)
    successful_calls = Column(BigInteger, default=0)
    failed_calls = Column(BigInteger, default=0)
    
    # Monitoring
    alerts_enabled = Column(Boolean, default=True)
    error_threshold_percentage = Column(Float, default=5.0)
    response_time_threshold_ms = Column(Integer, default=1000)
    
    # Lifecycle
    deprecated = Column(Boolean, default=False)
    deprecation_date = Column(DateTime(timezone=True))
    sunset_date = Column(DateTime(timezone=True))
    replacement_endpoint = Column(String(500))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    integration = relationship("Integration", back_populates="api_endpoints")
    api_calls = relationship("APICall", back_populates="endpoint")
    
    def __repr__(self):
        return f"<APIEndpoint(path='{self.endpoint_path}', method='{self.method}')>"

class APICall(BaseModel):
    """
    API call tracking for comprehensive monitoring!
    More detailed than Swiss API logging with legendary precision! 📊🔍
    """
    __tablename__ = "api_calls"
    
    # References
    endpoint_id = Column(Integer, ForeignKey("api_endpoints.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=True, index=True)
    
    # Call Details
    call_id = Column(String(100), unique=True, nullable=False, index=True)
    correlation_id = Column(String(100), index=True)
    request_timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    
    # Request Information
    request_method = Column(String(10), nullable=False)
    request_path = Column(String(500), nullable=False)
    request_headers = Column(JSON)
    request_body = Column(Text)
    request_size_bytes = Column(Integer)
    
    # Client Information
    client_ip = Column(String(45))  # IPv6 support
    user_agent = Column(Text)
    api_key_id = Column(String(100))
    client_application = Column(String(200))
    client_version = Column(String(50))
    
    # Response Information
    response_status_code = Column(Integer, nullable=False)
    response_headers = Column(JSON)
    response_body = Column(Text)
    response_size_bytes = Column(Integer)
    response_time_ms = Column(Integer)
    
    # Processing Details
    processing_time_ms = Column(Integer)
    database_time_ms = Column(Integer)
    external_api_time_ms = Column(Integer)
    cache_hit = Column(Boolean, default=False)
    
    # Error Information
    error_code = Column(String(50))
    error_message = Column(Text)
    error_details = Column(JSON)
    stack_trace = Column(Text)
    
    # Rate Limiting
    rate_limit_applied = Column(Boolean, default=False)
    rate_limit_remaining = Column(Integer)
    rate_limit_reset_timestamp = Column(DateTime(timezone=True))
    
    # Security
    authentication_method = Column(String(50))
    authorization_granted = Column(Boolean, default=True)
    security_warnings = Column(JSON)
    
    # Business Context
    business_context = Column(JSON)  # Business-specific metadata
    feature_flags = Column(JSON)     # Feature flags active during call
    
    # Relationships
    endpoint = relationship("APIEndpoint", back_populates="api_calls")
    user = relationship("User")
    integration = relationship("Integration")
    
    def __repr__(self):
        return f"<APICall(call_id='{self.call_id}', status={self.response_status_code})>"

class SyncLog(BaseModel):
    """
    Data synchronization logs for integration monitoring!
    More synchronized than Swiss precision timing! ⏰🔄
    """
    __tablename__ = "sync_logs"
    
    # References
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=False, index=True)
    
    # Sync Details
    sync_id = Column(String(100), unique=True, nullable=False, index=True)
    sync_type = Column(String(30), nullable=False)  # full, incremental, delta
    sync_direction = Column(String(20), nullable=False)  # inbound, outbound, bidirectional
    
    # Timeline
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    
    # Data Volume
    records_processed = Column(BigInteger, default=0)
    records_successful = Column(BigInteger, default=0)
    records_failed = Column(BigInteger, default=0)
    records_skipped = Column(BigInteger, default=0)
    
    # Data Transfer
    data_sent_bytes = Column(BigInteger, default=0)
    data_received_bytes = Column(BigInteger, default=0)
    api_calls_made = Column(Integer, default=0)
    
    # Status and Results
    status = Column(String(20), default="running")  # running, completed, failed, cancelled
    success_rate_percentage = Column(Float)
    error_summary = Column(JSON)  # Summary of errors encountered
    
    # Performance Metrics
    average_record_processing_time_ms = Column(Float)
    throughput_records_per_second = Column(Float)
    peak_memory_usage_mb = Column(Float)
    
    # Synchronization Metadata
    last_sync_token = Column(String(500))  # Token for incremental sync
    sync_checkpoints = Column(JSON)        # Checkpoints during sync
    data_consistency_checks = Column(JSON) # Data validation results
    
    # Error Details
    error_log = Column(Text)
    failed_records = Column(JSON)  # Details of failed records
    retry_count = Column(Integer, default=0)
    
    # Relationships
    integration = relationship("Integration", back_populates="sync_logs")
    
    def __repr__(self):
        return f"<SyncLog(sync_id='{self.sync_id}', status='{self.status}')>"

class Webhook(BaseModel):
    """
    Webhook configurations for real-time event notifications!
    More responsive than Swiss real-time communications! 📡⚡
    """
    __tablename__ = "webhooks"
    
    # Basic Configuration
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    webhook_url = Column(String(500), nullable=False)
    
    # Event Configuration
    event_types = Column(JSON, nullable=False)  # List of events to listen for
    event_filters = Column(JSON)  # Filters to apply to events
    payload_template = Column(JSON)  # Custom payload template
    
    # HTTP Configuration
    http_method = Column(String(10), default="POST")
    headers = Column(JSON)  # Custom headers to send
    authentication_type = Column(String(30))  # AuthenticationType enum
    authentication_config = Column(JSON)  # Auth configuration
    
    # Delivery Configuration
    timeout_seconds = Column(Integer, default=30)
    retry_attempts = Column(Integer, default=3)
    retry_backoff_seconds = Column(Integer, default=60)
    delivery_order = Column(String(20), default="at_least_once")  # at_least_once, exactly_once
    
    # Content Configuration
    content_type = Column(String(50), default="application/json")
    encoding = Column(String(20), default="utf-8")
    signature_secret = Column(String(200))  # Secret for payload signing
    include_metadata = Column(Boolean, default=True)
    
    # Delivery Tracking
    total_deliveries = Column(BigInteger, default=0)
    successful_deliveries = Column(BigInteger, default=0)
    failed_deliveries = Column(BigInteger, default=0)
    last_delivery_at = Column(DateTime(timezone=True))
    last_successful_delivery_at = Column(DateTime(timezone=True))
    
    # Performance Metrics
    average_delivery_time_ms = Column(Float)
    success_rate_percentage = Column(Float)
    
    # Monitoring
    health_check_enabled = Column(Boolean, default=True)
    alert_on_failure = Column(Boolean, default=True)
    failure_threshold = Column(Integer, default=5)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    owner = relationship("Employee", foreign_keys=[owner_id])
    deliveries = relationship("WebhookDelivery", back_populates="webhook")
    
    def __repr__(self):
        return f"<Webhook(name='{self.name}', url='{self.webhook_url}')>"

class WebhookDelivery(BaseModel):
    """
    Individual webhook delivery attempts with detailed tracking!
    More reliable than Swiss delivery services! 📦✅
    """
    __tablename__ = "webhook_deliveries"
    
    # References
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False, index=True)
    
    # Delivery Details
    delivery_id = Column(String(100), unique=True, nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    event_id = Column(String(100), nullable=False)
    
    # Attempt Information
    attempt_number = Column(Integer, default=1)
    attempted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Request Details
    request_url = Column(String(500), nullable=False)
    request_method = Column(String(10), nullable=False)
    request_headers = Column(JSON)
    request_payload = Column(Text)
    request_size_bytes = Column(Integer)
    
    # Response Details
    response_status_code = Column(Integer)
    response_headers = Column(JSON)
    response_body = Column(Text)
    response_time_ms = Column(Integer)
    
    # Status
    status = Column(String(20), default="pending")  # pending, delivered, failed, cancelled
    error_message = Column(Text)
    error_details = Column(JSON)
    
    # Next Retry
    next_retry_at = Column(DateTime(timezone=True))
    
    # Relationships
    webhook = relationship("Webhook", back_populates="deliveries")
    
    def __repr__(self):
        return f"<WebhookDelivery(delivery_id='{self.delivery_id}', status='{self.status}')>"

class DataTransformation(BaseModel):
    """
    Data transformation rules for seamless integration!
    More elegant than Swiss data transformation with legendary precision! 🔄💎
    """
    __tablename__ = "data_transformations"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    transformation_code = Column(String(50), unique=True, index=True)
    
    # Source and Target
    source_system = Column(String(100), nullable=False)
    target_system = Column(String(100), nullable=False)
    source_format = Column(String(50), nullable=False)  # json, xml, csv, etc.
    target_format = Column(String(50), nullable=False)
    
    # Transformation Rules
    transformation_rules = Column(JSON, nullable=False)  # Detailed transformation logic
    field_mappings = Column(JSON)      # Direct field mappings
    data_validations = Column(JSON)    # Validation rules
    business_rules = Column(JSON)      # Business logic rules
    
    # Processing Configuration
    batch_processing = Column(Boolean, default=False)
    real_time_processing = Column(Boolean, default=True)
    parallel_processing = Column(Boolean, default=False)
    max_parallel_threads = Column(Integer, default=4)
    
    # Error Handling
    error_handling_strategy = Column(String(30), default="skip")  # skip, fail, transform
    validation_mode = Column(String(20), default="strict")  # strict, lenient, custom
    default_values = Column(JSON)  # Default values for missing fields
    
    # Performance Metrics
    total_transformations = Column(BigInteger, default=0)
    successful_transformations = Column(BigInteger, default=0)
    failed_transformations = Column(BigInteger, default=0)
    average_processing_time_ms = Column(Float)
    
    # Monitoring
    performance_monitoring = Column(Boolean, default=True)
    data_quality_monitoring = Column(Boolean, default=True)
    alert_on_failure_rate = Column(Float, default=5.0)  # Alert if failure rate exceeds %
    
    # Ownership
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    version = Column(String(20), default="1.0")
    
    # Relationships
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    
    def __repr__(self):
        return f"<DataTransformation(name='{self.name}', source='{self.source_system}', target='{self.target_system}')>"

# Add relationships to Employee model (if not already added)
# Employee.owned_integrations = relationship("Integration", foreign_keys="Integration.owner_id")
# Employee.technical_integrations = relationship("Integration", foreign_keys="Integration.technical_contact_id")
# Employee.business_integrations = relationship("Integration", foreign_keys="Integration.business_contact_id")
# Employee.owned_webhooks = relationship("Webhook", foreign_keys="Webhook.owner_id")
# Employee.created_transformations = relationship("DataTransformation", foreign_keys="DataTransformation.created_by_id")