"""
LEGENDARY ENTERPRISE ANALYTICS & REPORTING MODELS 📊🚀
More insightful than a Swiss data analyst with legendary intelligence!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 2.5+ HOUR CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 02:37:23 UTC - WE'RE ANALYZING EVERYTHING!
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

class ReportType(enum.Enum):
    """Report types - more organized than a Swiss data library!"""
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    HR_METRICS = "hr_metrics"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    EXECUTIVE = "executive"
    CUSTOM = "custom"
    REAL_TIME = "real_time"

class ReportFrequency(enum.Enum):
    """Report frequency scheduling"""
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"
    ON_DEMAND = "on_demand"

class DataSourceType(enum.Enum):
    """Data source types for analytics"""
    DATABASE = "database"
    API = "api"
    FILE_UPLOAD = "file_upload"
    EXTERNAL_SERVICE = "external_service"
    REAL_TIME_STREAM = "real_time_stream"
    MANUAL_ENTRY = "manual_entry"

class VisualizationType(enum.Enum):
    """Chart and visualization types"""
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    HEAT_MAP = "heat_map"
    GAUGE = "gauge"
    TABLE = "table"
    KPI_CARD = "kpi_card"
    FUNNEL = "funnel"
    AREA_CHART = "area_chart"

class Dashboard(BaseModel):
    """
    Analytics dashboards that are more insightful than Swiss data centers!
    More comprehensive than a legendary business intelligence platform! 📊✨
    """
    __tablename__ = "dashboards"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    dashboard_code = Column(String(50), unique=True, index=True)
    
    # Dashboard Properties
    dashboard_type = Column(String(30), nullable=False)  # ReportType enum
    category = Column(String(100))  # HR, Finance, Operations, etc.
    tags = Column(JSON)  # List of tags for searching
    
    # Layout and Design
    layout_config = Column(JSON, nullable=False)  # Dashboard layout configuration
    theme = Column(String(50), default="corporate")
    color_scheme = Column(JSON)  # Custom color scheme
    
    # Access Control
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    is_public = Column(Boolean, default=False)
    shared_with_departments = Column(JSON)  # List of department IDs
    shared_with_roles = Column(JSON)       # List of job roles
    shared_with_users = Column(JSON)       # List of specific user IDs
    
    # Refresh and Data
    auto_refresh_minutes = Column(Integer, default=60)  # Auto-refresh interval
    last_refreshed_at = Column(DateTime(timezone=True))
    data_retention_days = Column(Integer, default=365)
    
    # Performance
    load_time_ms = Column(Integer)  # Last load time in milliseconds
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="dashboard")
    
    def __repr__(self):
        return f"<Dashboard(name='{self.name}', type='{self.dashboard_type}')>"

class DashboardWidget(BaseModel):
    """
    Dashboard widgets for modular analytics!
    More flexible than Swiss data visualization tools! 📈🔧
    """
    __tablename__ = "dashboard_widgets"
    
    # References
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"), nullable=False, index=True)
    
    # Widget Properties
    widget_name = Column(String(200), nullable=False)
    widget_type = Column(String(30), nullable=False)  # VisualizationType enum
    description = Column(Text)
    
    # Position and Size
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer, default=4)   # Grid units
    height = Column(Integer, default=3)  # Grid units
    z_index = Column(Integer, default=1)
    
    # Data Configuration
    data_source_config = Column(JSON, nullable=False)  # Data source and query configuration
    visualization_config = Column(JSON)  # Chart/visualization specific settings
    filter_config = Column(JSON)  # Available filters for this widget
    
    # Styling
    custom_styling = Column(JSON)  # Custom CSS/styling options
    title_visible = Column(Boolean, default=True)
    border_visible = Column(Boolean, default=True)
    
    # Interactivity
    is_interactive = Column(Boolean, default=True)
    drill_down_enabled = Column(Boolean, default=False)
    drill_down_config = Column(JSON)  # Drill-down configuration
    
    # Performance
    cache_duration_minutes = Column(Integer, default=30)
    last_updated_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets")
    
    def __repr__(self):
        return f"<DashboardWidget(name='{self.widget_name}', type='{self.widget_type}')>"

class Report(BaseModel):
    """
    Scheduled and on-demand reports!
    More comprehensive than Swiss business reporting! 📋📊
    """
    __tablename__ = "reports"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    report_code = Column(String(50), unique=True, index=True)
    
    # Report Configuration
    report_type = Column(String(30), nullable=False)  # ReportType enum
    category = Column(String(100))
    template_id = Column(Integer, nullable=True)  # Reference to report template
    
    # Data Source
    data_source_config = Column(JSON, nullable=False)  # Data source configuration
    parameters = Column(JSON)  # Report parameters and filters
    
    # Scheduling
    frequency = Column(String(20), default="on_demand")  # ReportFrequency enum
    schedule_config = Column(JSON)  # Cron-like scheduling configuration
    next_run_at = Column(DateTime(timezone=True))
    last_run_at = Column(DateTime(timezone=True))
    
    # Output Configuration
    output_formats = Column(JSON, default=["pdf", "excel"])  # Supported output formats
    email_recipients = Column(JSON)  # List of email addresses
    storage_location = Column(String(500))  # Where to store generated reports
    
    # Dashboard Integration
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"), nullable=True, index=True)
    auto_publish_to_dashboard = Column(Boolean, default=False)
    
    # Access Control
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    is_public = Column(Boolean, default=False)
    shared_with_departments = Column(JSON)
    shared_with_roles = Column(JSON)
    
    # Performance Tracking
    average_generation_time_ms = Column(Integer)
    last_generation_time_ms = Column(Integer)
    execution_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="reports")
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    executions = relationship("ReportExecution", back_populates="report")
    
    def __repr__(self):
        return f"<Report(name='{self.name}', type='{self.report_type}')>"

class ReportExecution(BaseModel):
    """
    Report execution history and results!
    More detailed than Swiss execution tracking! 📈⚡
    """
    __tablename__ = "report_executions"
    
    # References
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False, index=True)
    executed_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    
    # Execution Details
    execution_type = Column(String(20), default="scheduled")  # scheduled, manual, api
    started_at = Column(DateTime(timezone=True), nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(Integer)
    
    # Parameters and Filters
    execution_parameters = Column(JSON)  # Parameters used for this execution
    applied_filters = Column(JSON)       # Filters applied during execution
    
    # Results
    status = Column(String(20), default="running")  # running, completed, failed, cancelled
    rows_processed = Column(BigInteger)
    output_file_urls = Column(JSON)  # URLs to generated output files
    output_size_bytes = Column(BigInteger)
    
    # Error Handling
    error_message = Column(Text)
    error_details = Column(JSON)
    retry_count = Column(Integer, default=0)
    
    # Performance Metrics
    data_fetch_time_ms = Column(Integer)
    processing_time_ms = Column(Integer)
    rendering_time_ms = Column(Integer)
    
    # Distribution
    email_sent_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    
    # Relationships
    report = relationship("Report", back_populates="executions")
    executed_by = relationship("Employee", foreign_keys=[executed_by_id])
    
    def __repr__(self):
        return f"<ReportExecution(report_id={self.report_id}, status='{self.status}')>"

class DataSource(BaseModel):
    """
    Data sources for analytics and reporting!
    More connected than Swiss data integration hubs! 🔗📊
    """
    __tablename__ = "data_sources"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    source_code = Column(String(50), unique=True, index=True)
    
    # Source Configuration
    source_type = Column(String(30), nullable=False)  # DataSourceType enum
    connection_config = Column(JSON, nullable=False)  # Connection parameters
    authentication_config = Column(JSON)  # Auth credentials (encrypted)
    
    # Data Schema
    schema_definition = Column(JSON)  # Data schema and field definitions
    available_tables = Column(JSON)  # Available tables/endpoints
    sample_data = Column(JSON)       # Sample data for preview
    
    # Refresh and Sync
    refresh_frequency = Column(String(20), default="daily")  # How often to refresh
    last_sync_at = Column(DateTime(timezone=True))
    last_successful_sync_at = Column(DateTime(timezone=True))
    next_sync_at = Column(DateTime(timezone=True))
    
    # Performance
    average_query_time_ms = Column(Integer)
    total_queries_executed = Column(BigInteger, default=0)
    data_size_mb = Column(Float)
    
    # Health Monitoring
    is_healthy = Column(Boolean, default=True, index=True)
    health_check_url = Column(String(500))
    last_health_check_at = Column(DateTime(timezone=True))
    consecutive_failures = Column(Integer, default=0)
    
    # Access Control
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    is_public = Column(Boolean, default=False)
    allowed_departments = Column(JSON)
    allowed_roles = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    
    def __repr__(self):
        return f"<DataSource(name='{self.name}', type='{self.source_type}')>"

class MetricDefinition(BaseModel):
    """
    Business metric definitions for consistent reporting!
    More precise than Swiss measurement standards! 📏📊
    """
    __tablename__ = "metric_definitions"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    metric_code = Column(String(50), unique=True, index=True)
    
    # Metric Properties
    category = Column(String(100), nullable=False)  # HR, Finance, Operations, etc.
    metric_type = Column(String(30), nullable=False)  # count, sum, average, percentage, ratio
    unit_of_measurement = Column(String(50))  # dollars, hours, percentage, etc.
    
    # Calculation
    calculation_formula = Column(Text, nullable=False)  # SQL or formula for calculation
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=False, index=True)
    dependencies = Column(JSON)  # Other metrics this depends on
    
    # Formatting and Display
    display_format = Column(String(50))  # currency, percentage, decimal, etc.
    decimal_places = Column(Integer, default=2)
    prefix = Column(String(10))  # $, %, etc.
    suffix = Column(String(10))  # K, M, B for thousands/millions/billions
    
    # Thresholds and Targets
    target_value = Column(Float)
    warning_threshold = Column(Float)
    critical_threshold = Column(Float)
    threshold_direction = Column(String(10), default="higher")  # higher, lower
    
    # Aggregation
    default_aggregation = Column(String(20), default="sum")  # sum, avg, count, min, max
    time_aggregation = Column(String(20), default="daily")   # hourly, daily, weekly, monthly
    supports_drill_down = Column(Boolean, default=False)
    drill_down_dimensions = Column(JSON)  # Available drill-down dimensions
    
    # Access Control
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    is_public = Column(Boolean, default=True)
    restricted_to_departments = Column(JSON)
    
    # Status and Versioning
    version = Column(String(20), default="1.0")
    is_active = Column(Boolean, default=True, index=True)
    deprecated_at = Column(DateTime(timezone=True))
    replacement_metric_id = Column(Integer, ForeignKey("metric_definitions.id"), nullable=True)
    
    # Relationships
    data_source = relationship("DataSource")
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    replacement_metric = relationship("MetricDefinition", remote_side="MetricDefinition.id")
    
    def __repr__(self):
        return f"<MetricDefinition(name='{self.name}', type='{self.metric_type}')>"

class AnalyticsEvent(BaseModel):
    """
    Real-time analytics events for live tracking!
    More responsive than Swiss real-time monitoring! ⚡📊
    """
    __tablename__ = "analytics_events"
    
    # Event Details
    event_name = Column(String(100), nullable=False, index=True)
    event_category = Column(String(50), nullable=False, index=True)
    event_type = Column(String(30), nullable=False)  # user_action, system_event, business_event
    
    # Event Data
    event_data = Column(JSON, nullable=False)  # Event payload
    event_value = Column(Float)  # Numeric value associated with event
    event_currency = Column(String(10))  # Currency for financial events
    
    # Context
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    session_id = Column(String(100), index=True)
    
    # Source Information
    source_system = Column(String(100), nullable=False)  # Which system generated the event
    source_version = Column(String(20))  # Version of the source system
    api_version = Column(String(20))     # API version used
    
    # Technical Details
    ip_address = Column(String(45))  # IPv6 support
    user_agent = Column(Text)
    device_type = Column(String(50))  # desktop, mobile, tablet
    browser = Column(String(100))
    
    # Geolocation
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    timezone = Column(String(50))
    
    # Timing
    event_timestamp = Column(DateTime(timezone=True), nullable=False, index=True, server_default=func.now())
    processing_timestamp = Column(DateTime(timezone=True))
    
    # Processing Status
    is_processed = Column(Boolean, default=False, index=True)
    processing_errors = Column(JSON)  # Any errors during processing
    
    # Relationships
    user = relationship("User")
    employee = relationship("Employee")
    
    def __repr__(self):
        return f"<AnalyticsEvent(name='{self.event_name}', category='{self.event_category}')>"

class UserAnalyticsPreference(BaseModel):
    """
    User preferences for analytics and reporting!
    More personalized than Swiss customization options! 👤📊
    """
    __tablename__ = "user_analytics_preferences"
    
    # References
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Dashboard Preferences
    default_dashboard_id = Column(Integer, ForeignKey("dashboards.id"), nullable=True)
    favorite_dashboards = Column(JSON, default=[])  # List of dashboard IDs
    dashboard_refresh_preference = Column(String(20), default="auto")  # auto, manual, scheduled
    
    # Report Preferences
    favorite_reports = Column(JSON, default=[])  # List of report IDs
    default_output_format = Column(String(20), default="pdf")
    email_notifications_enabled = Column(Boolean, default=True)
    
    # Display Preferences
    theme_preference = Column(String(50), default="light")  # light, dark, auto
    timezone = Column(String(50), default="UTC")
    date_format = Column(String(20), default="YYYY-MM-DD")
    number_format = Column(String(20), default="en-US")  # Locale for number formatting
    
    # Data Preferences
    default_date_range = Column(String(20), default="last_30_days")
    data_refresh_frequency = Column(String(20), default="hourly")
    cache_preference = Column(String(20), default="balanced")  # speed, accuracy, balanced
    
    # Privacy Preferences
    analytics_tracking_enabled = Column(Boolean, default=True)
    usage_data_sharing = Column(Boolean, default=True)
    personalization_enabled = Column(Boolean, default=True)
    
    # Alert Preferences
    alert_threshold_preferences = Column(JSON)  # Custom alert thresholds
    alert_delivery_methods = Column(JSON, default=["email", "in_app"])
    quiet_hours_start = Column(String(10))  # "22:00" format
    quiet_hours_end = Column(String(10))    # "08:00" format
    
    # Relationships
    user = relationship("User")
    default_dashboard = relationship("Dashboard")
    
    def __repr__(self):
        return f"<UserAnalyticsPreference(user_id={self.user_id})>"

# Add relationships to Employee model (if not already added)
# Employee.created_dashboards = relationship("Dashboard", foreign_keys="Dashboard.created_by_id")
# Employee.created_reports = relationship("Report", foreign_keys="Report.created_by_id")
# Employee.report_executions = relationship("ReportExecution", foreign_keys="ReportExecution.executed_by_id")
# Employee.created_data_sources = relationship("DataSource", foreign_keys="DataSource.created_by_id")
# Employee.created_metrics = relationship("MetricDefinition", foreign_keys="MetricDefinition.created_by_id")
# Employee.analytics_events = relationship("AnalyticsEvent", foreign_keys="AnalyticsEvent.employee_id")