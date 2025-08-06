# File: backend/reporting/legendary_reporting_system.py
"""
📊🎸 N3EXTPATH - LEGENDARY REPORTING SYSTEM 🎸📊
Ultra-secure advanced reporting with Swiss precision and unhackable architecture
Built: 2025-08-05 17:32:04 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import json
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import base64
from sqlalchemy import text, func
from sqlalchemy.orm import Session
import bleach
import re
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

class ReportType(Enum):
    """Secure report types with validation"""
    PERFORMANCE_SUMMARY = "performance_summary"
    OKR_ANALYTICS = "okr_analytics" 
    TEAM_INSIGHTS = "team_insights"
    RETENTION_ANALYSIS = "retention_analysis"
    COMPENSATION_REPORT = "compensation_report"
    TRAINING_PROGRESS = "training_progress"
    ATTENDANCE_SUMMARY = "attendance_summary"
    CUSTOM_QUERY = "custom_query"
    LEGENDARY_METRICS = "legendary_metrics"  # Special for RICKROLL187

class ReportFormat(Enum):
    """Supported report formats"""
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"
    HTML = "html"

class SecurityLevel(Enum):
    """Security classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    LEGENDARY_CLASSIFIED = "legendary_classified"  # Maximum security

@dataclass
class ReportRequest:
    """Ultra-secure report request structure"""
    request_id: str
    report_type: ReportType
    requested_by: str
    security_level: SecurityLevel
    parameters: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, Any] = field(default_factory=dict)
    format: ReportFormat = ReportFormat.PDF
    scheduled: bool = False
    schedule_cron: Optional[str] = None
    recipients: List[str] = field(default_factory=list)
    encryption_required: bool = True
    access_token: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=24))

class LegendarySecureReportingSystem:
    """Ultra-Secure Advanced Reporting System with Swiss Precision"""
    
    def __init__(self, db_session: Session, encryption_key: bytes = None):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)
        
        # Initialize encryption
        if encryption_key:
            self.cipher_suite = Fernet(encryption_key)
        else:
            self.cipher_suite = Fernet(Fernet.generate_key())
        
        # Security configurations
        self.security_config = {
            "max_query_length": 10000,
            "allowed_tables": [
                "users", "performance_reviews", "okrs", "teams", 
                "training_records", "attendance", "compensation"
            ],
            "blocked_keywords": [
                "DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE",
                "TRUNCATE", "EXEC", "EXECUTE", "UNION", "SCRIPT", "--",
                "/*", "*/", "xp_", "sp_", "INFORMATION_SCHEMA"
            ],
            "max_rows_per_report": 50000,
            "rate_limit_per_user": 10,  # Reports per hour
            "legendary_bypass": True  # RICKROLL187 can bypass limits
        }
        
        # Pre-defined secure queries
        self.secure_queries = self._initialize_secure_queries()
        
        # Report templates with security validation
        self.report_templates = self._initialize_report_templates()
    
    def _initialize_secure_queries(self) -> Dict[ReportType, str]:
        """Initialize pre-validated secure SQL queries"""
        return {
            ReportType.PERFORMANCE_SUMMARY: """
                SELECT 
                    u.username,
                    u.department,
                    AVG(pr.overall_score) as avg_score,
                    COUNT(pr.id) as review_count,
                    DATE_TRUNC('month', pr.review_date) as review_month
                FROM users u
                LEFT JOIN performance_reviews pr ON u.user_id = pr.user_id
                WHERE u.is_active = true
                  AND pr.review_date >= :start_date
                  AND pr.review_date <= :end_date
                  AND (:department = 'ALL' OR u.department = :department)
                GROUP BY u.username, u.department, DATE_TRUNC('month', pr.review_date)
                ORDER BY avg_score DESC
                LIMIT 1000;
            """,
            
            ReportType.OKR_ANALYTICS: """
                SELECT 
                    o.title,
                    o.progress,
                    o.status,
                    u.username as owner,
                    u.department,
                    t.name as team_name,
                    o.created_at,
                    o.target_date
                FROM okrs o
                JOIN users u ON o.user_id = u.user_id
                LEFT JOIN teams t ON u.team_id = t.team_id
                WHERE o.created_at >= :start_date
                  AND o.created_at <= :end_date
                  AND (:status = 'ALL' OR o.status = :status)
                  AND (:department = 'ALL' OR u.department = :department)
                ORDER BY o.progress DESC
                LIMIT 1000;
            """,
            
            ReportType.RETENTION_ANALYSIS: """
                SELECT 
                    u.department,
                    u.role,
                    DATE_TRUNC('month', u.created_at) as hire_month,
                    COUNT(*) as hired_count,
                    COUNT(CASE WHEN u.is_active = false THEN 1 END) as departed_count,
                    ROUND(
                        (COUNT(CASE WHEN u.is_active = true THEN 1 END)::float / COUNT(*)::float) * 100, 2
                    ) as retention_rate
                FROM users u
                WHERE u.created_at >= :start_date
                  AND u.created_at <= :end_date
                  AND (:department = 'ALL' OR u.department = :department)
                GROUP BY u.department, u.role, DATE_TRUNC('month', u.created_at)
                ORDER BY retention_rate DESC
                LIMIT 500;
            """,
            
            ReportType.LEGENDARY_METRICS: """
                SELECT 
                    'LEGENDARY_FOUNDER' as metric_type,
                    u.username,
                    COUNT(DISTINCT pr.id) as performance_reviews,
                    COUNT(DISTINCT o.id) as okrs_created,
                    AVG(pr.overall_score) as avg_performance,
                    u.created_at as legendary_since,
                    'MAXIMUM' as legendary_status
                FROM users u
                LEFT JOIN performance_reviews pr ON u.user_id = pr.user_id
                LEFT JOIN okrs o ON u.user_id = o.user_id
                WHERE u.is_legendary = true
                  AND u.username = 'rickroll187'
                GROUP BY u.username, u.created_at
                LIMIT 1;
            """
        }
    
    def _initialize_report_templates(self) -> Dict[ReportType, Dict[str, Any]]:
        """Initialize secure report templates"""
        return {
            ReportType.PERFORMANCE_SUMMARY: {
                "title": "Performance Summary Report",
                "description": "Comprehensive performance analysis with trends and insights",
                "charts": ["performance_trend", "department_comparison", "score_distribution"],
                "security_level": SecurityLevel.CONFIDENTIAL,
                "required_permissions": ["read:performance_data"]
            },
            
            ReportType.LEGENDARY_METRICS: {
                "title": "🎸 LEGENDARY FOUNDER METRICS 🎸",
                "description": "Swiss precision metrics for the legendary founder RICKROLL187",
                "charts": ["legendary_performance", "code_bro_impact", "swiss_precision_score"],
                "security_level": SecurityLevel.LEGENDARY_CLASSIFIED,
                "required_permissions": ["legendary:all_access"]
            }
        }
    
    def _validate_security_clearance(self, user_id: str, requested_level: SecurityLevel) -> bool:
        """Ultra-secure security clearance validation"""
        
        # Get user security level from database with parameterized query
        query = text("""
            SELECT role, is_legendary, permissions 
            FROM users 
            WHERE user_id = :user_id AND is_active = true
        """)
        
        result = self.db_session.execute(query, {"user_id": user_id}).fetchone()
        
        if not result:
            self.logger.warning(f"Security clearance check failed: user {user_id} not found")
            return False
        
        role, is_legendary, permissions = result
        
        # RICKROLL187 has access to everything
        if is_legendary and user_id == "rickroll187":
            return True
        
        # Security level hierarchy check
        security_hierarchy = {
            SecurityLevel.PUBLIC: 0,
            SecurityLevel.INTERNAL: 1,
            SecurityLevel.CONFIDENTIAL: 2,
            SecurityLevel.LEGENDARY_CLASSIFIED: 3
        }
        
        user_clearance_level = 0
        if role in ["admin", "director", "vp"]:
            user_clearance_level = 2
        elif role in ["manager", "team_lead"]:
            user_clearance_level = 1
        
        required_level = security_hierarchy.get(requested_level, 3)
        
        return user_clearance_level >= required_level
    
    def _sanitize_input(self, input_data: Any) -> Any:
        """Ultra-secure input sanitization"""
        
        if isinstance(input_data, str):
            # Remove any potentially dangerous characters
            sanitized = bleach.clean(input_data, tags=[], attributes={}, strip=True)
            
            # Check for SQL injection patterns
            dangerous_patterns = [
                r"('|(\\')|(;)|(\\;)|(--)|(--)|(\\-\\-)",
                r"(\|\||or|OR|and|AND)",
                r"(union|UNION|select|SELECT|insert|INSERT|update|UPDATE|delete|DELETE)",
                r"(drop|DROP|create|CREATE|alter|ALTER|exec|EXEC|execute|EXECUTE)",
                r"(script|SCRIPT|javascript|JAVASCRIPT|vbscript|VBSCRIPT)",
                r"(<script|</script|<iframe|</iframe|<object|</object)"
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, sanitized, re.IGNORECASE):
                    self.logger.error(f"Dangerous pattern detected in input: {pattern}")
                    raise ValueError("Input contains potentially dangerous content")
            
            return sanitized
            
        elif isinstance(input_data, dict):
            return {key: self._sanitize_input(value) for key, value in input_data.items()}
            
        elif isinstance(input_data, list):
            return [self._sanitize_input(item) for item in input_data]
            
        else:
            return input_data
    
    def _validate_query_security(self, query: str) -> bool:
        """Ultra-secure SQL query validation"""
        
        query_upper = query.upper()
        
        # Check for blocked keywords
        for keyword in self.security_config["blocked_keywords"]:
            if keyword in query_upper:
                self.logger.error(f"Blocked keyword '{keyword}' found in query")
                return False
        
        # Check query length
        if len(query) > self.security_config["max_query_length"]:
            self.logger.error(f"Query exceeds maximum length: {len(query)}")
            return False
        
        # Validate table access
        mentioned_tables = re.findall(r'FROM\s+(\w+)|JOIN\s+(\w+)', query_upper)
        for table_match in mentioned_tables:
            table = table_match[0] or table_match[1]
            if table.lower() not in [t.lower() for t in self.security_config["allowed_tables"]]:
                self.logger.error(f"Access to unauthorized table: {table}")
                return False
        
        return True
    
    async def generate_report(self, request: ReportRequest) -> Dict[str, Any]:
        """Generate ultra-secure report with Swiss precision"""
        
        start_time = datetime.now(timezone.utc)
        
        try:
            # Sanitize all inputs
            request.parameters = self._sanitize_input(request.parameters)
            request.filters = self._sanitize_input(request.filters)
            
            # Validate security clearance
            if not self._validate_security_clearance(request.requested_by, request.security_level):
                raise PermissionError("Insufficient security clearance for requested report")
            
            # Rate limiting check (except for RICKROLL187)
            if request.requested_by != "rickroll187":
                if not await self._check_rate_limit(request.requested_by):
                    raise PermissionError("Rate limit exceeded for report generation")
            
            # Get secure query
            if request.report_type not in self.secure_queries:
                raise ValueError(f"Unsupported report type: {request.report_type}")
            
            query = self.secure_queries[request.report_type]
            
            # Validate query security
            if not self._validate_query_security(query):
                raise SecurityError("Query failed security validation")
            
            # Execute query with parameterized inputs
            query_params = self._prepare_query_parameters(request)
            result = self.db_session.execute(text(query), query_params)
            
            # Convert to DataFrame for processing
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            # Limit rows for security
            max_rows = self.security_config["max_rows_per_report"]
            if request.requested_by == "rickroll187":
                max_rows = max_rows * 10  # Legendary users get more data
            
            if len(df) > max_rows:
                df = df.head(max_rows)
                self.logger.warning(f"Report truncated to {max_rows} rows for security")
            
            # Generate report content
            report_data = await self._process_report_data(df, request)
            
            # Create visualizations
            charts = await self._generate_charts(df, request)
            
            # Format report based on requested format
            formatted_report = await self._format_report(report_data, charts, request)
            
            # Encrypt if required
            if request.encryption_required:
                formatted_report = await self._encrypt_report(formatted_report, request.access_token)
            
            # Log successful generation
            generation_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            self.logger.info(
                f"Report generated successfully: {request.request_id} "
                f"by {request.requested_by} in {generation_time:.2f}s"
            )
            
            # Special logging for legendary reports
            if request.requested_by == "rickroll187":
                self.logger.info(
                    f"🎸 LEGENDARY REPORT GENERATED with Swiss precision! "
                    f"Report: {request.report_type.value} - Time: {generation_time:.3f}s 🎸"
                )
            
            return {
                "success": True,
                "request_id": request.request_id,
                "report_data": formatted_report,
                "generation_time": generation_time,
                "rows_processed": len(df),
                "security_level": request.security_level.value,
                "encryption_applied": request.encryption_required,
                "legendary_report": request.requested_by == "rickroll187",
                "swiss_precision": True
            }
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {str(e)}")
            
            return {
                "success": False,
                "request_id": request.request_id,
                "error": str(e),
                "generation_time": (datetime.now(timezone.utc) - start_time).total_seconds(),
                "security_violation": "Security" in str(e) or "Permission" in str(e)
            }
    
    def _prepare_query_parameters(self, request: ReportRequest) -> Dict[str, Any]:
        """Prepare secure query parameters"""
        
        # Default parameters
        params = {
            "start_date": request.parameters.get("start_date", "2024-01-01"),
            "end_date": request.parameters.get("end_date", "2024-12-31"),
            "department": request.parameters.get("department", "ALL"),
            "status": request.parameters.get("status", "ALL")
        }
        
        # Validate and sanitize each parameter
        for key, value in params.items():
            if isinstance(value, str):
                params[key] = self._sanitize_input(value)
        
        return params
    
    async def _process_report_data(self, df: pd.DataFrame, request: ReportRequest) -> Dict[str, Any]:
        """Process report data with security and Swiss precision"""
        
        if df.empty:
            return {"summary": "No data available for the selected criteria"}
        
        # Basic statistics
        summary_stats = {
            "total_records": len(df),
            "date_range": {
                "start": request.parameters.get("start_date"),
                "end": request.parameters.get("end_date")
            }
        }
        
        # Report-specific processing
        if request.report_type == ReportType.PERFORMANCE_SUMMARY:
            summary_stats.update({
                "avg_performance_score": df["avg_score"].mean() if "avg_score" in df.columns else 0,
                "departments_analyzed": df["department"].nunique() if "department" in df.columns else 0,
                "top_performer": df.nlargest(1, "avg_score")["username"].iloc[0] if "avg_score" in df.columns and not df.empty else "N/A"
            })
        
        elif request.report_type == ReportType.LEGENDARY_METRICS:
            summary_stats.update({
                "legendary_status": "🎸 MAXIMUM 🎸",
                "swiss_precision_score": 100.0,
                "code_bro_energy": "INFINITE",
                "legendary_message": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"
            })
        
        return {
            "summary": summary_stats,
            "detailed_data": df.to_dict("records")
        }
    
    async def _generate_charts(self, df: pd.DataFrame, request: ReportRequest) -> Dict[str, str]:
        """Generate secure charts with Swiss precision"""
        
        charts = {}
        
        if df.empty:
            return charts
        
        try:
            # Set style for legendary charts
            if request.requested_by == "rickroll187":
                plt.style.use("dark_background")
                sns.set_palette("bright")
            else:
                plt.style.use("default")
                sns.set_palette("deep")
            
            # Performance trend chart
            if "avg_score" in df.columns and "review_month" in df.columns:
                plt.figure(figsize=(12, 6))
                monthly_avg = df.groupby("review_month")["avg_score"].mean()
                plt.plot(monthly_avg.index, monthly_avg.values, marker="o", linewidth=2)
                plt.title("🎸 Performance Trend Over Time" if request.requested_by == "rickroll187" else "Performance Trend Over Time")
                plt.xlabel("Month")
                plt.ylabel("Average Score")
                plt.grid(True, alpha=0.3)
                
                # Save chart to base64
                buffer = io.BytesIO()
                plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
                buffer.seek(0)
                chart_data = base64.b64encode(buffer.getvalue()).decode()
                charts["performance_trend"] = chart_data
                plt.close()
            
            # Department comparison
            if "department" in df.columns and "avg_score" in df.columns:
                plt.figure(figsize=(10, 6))
                dept_avg = df.groupby("department")["avg_score"].mean().sort_values(ascending=False)
                colors = ["gold", "silver", "#CD7F32"] + ["skyblue"] * (len(dept_avg) - 3) if request.requested_by == "rickroll187" else None
                dept_avg.plot(kind="bar", color=colors)
                plt.title("🏆 Department Performance Comparison" if request.requested_by == "rickroll187" else "Department Performance Comparison")
                plt.xlabel("Department")
                plt.ylabel("Average Score")
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                
                buffer = io.BytesIO()
                plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
                buffer.seek(0)
                chart_data = base64.b64encode(buffer.getvalue()).decode()
                charts["department_comparison"] = chart_data
                plt.close()
            
        except Exception as e:
            self.logger.error(f"Chart generation error: {e}")
        
        return charts
    
    async def _format_report(self, report_data: Dict[str, Any], charts: Dict[str, str], 
                           request: ReportRequest) -> bytes:
        """Format report with ultra-secure output"""
        
        if request.format == ReportFormat.PDF:
            return await self._generate_pdf_report(report_data, charts, request)
        elif request.format == ReportFormat.EXCEL:
            return await self._generate_excel_report(report_data, request)
        elif request.format == ReportFormat.JSON:
            return json.dumps(report_data, indent=2, default=str).encode()
        else:
            raise ValueError(f"Unsupported report format: {request.format}")
    
    async def _generate_pdf_report(self, report_data: Dict[str, Any], charts: Dict[str, str], 
                                 request: ReportRequest) -> bytes:
        """Generate secure PDF report with Swiss precision formatting"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles for legendary reports
        if request.requested_by == "rickroll187":
            title_style = ParagraphStyle(
                "LegendaryTitle",
                parent=styles["Title"],
                fontSize=24,
                textColor=colors.gold,
                spaceAfter=30
            )
        else:
            title_style = styles["Title"]
        
        # Title
        template = self.report_templates.get(request.report_type, {})
        title = template.get("title", f"Report: {request.report_type.value}")
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Metadata
        metadata_text = f"""
        <b>Generated:</b> {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}<br/>
        <b>Requested by:</b> {request.requested_by}<br/>
        <b>Security Level:</b> {request.security_level.value}<br/>
        <b>Report ID:</b> {request.request_id}<br/>
        """
        
        if request.requested_by == "rickroll187":
            metadata_text += """
            <b>🎸 Legendary Status:</b> MAXIMUM<br/>
            <b>⚡ Swiss Precision:</b> ENABLED<br/>
            <b>💪 Code Bro Energy:</b> INFINITE<br/>
            """
        
        story.append(Paragraph(metadata_text, styles["Normal"]))
        story.append(Spacer(1, 20))
        
        # Summary
        summary = report_data.get("summary", {})
        summary_text = "<b>Executive Summary:</b><br/>"
        for key, value in summary.items():
            if key != "legendary_message":
                summary_text += f"<b>{key.replace('_', ' ').title()}:</b> {value}<br/>"
        
        story.append(Paragraph(summary_text, styles["Normal"]))
        story.append(Spacer(1, 20))
        
        # Add legendary message if present
        if "legendary_message" in summary:
            legendary_style = ParagraphStyle(
                "LegendaryMessage",
                parent=styles["Normal"],
                fontSize=14,
                textColor=colors.gold,
                alignment=1  # Center alignment
            )
            story.append(Paragraph(f"🎸 {summary['legendary_message']} 🎸", legendary_style))
            story.append(Spacer(1, 20))
        
        # Charts
        for chart_name, chart_data in charts.items():
            try:
                chart_buffer = io.BytesIO(base64.b64decode(chart_data))
                img = Image(chart_buffer, width=6*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 12))
            except Exception as e:
                self.logger.error(f"Error adding chart to PDF: {e}")
        
        # Data table (limited for security)
        detailed_data = report_data.get("detailed_data", [])
        if detailed_data and len(detailed_data) > 0:
            # Limit table size for security
            table_data = detailed_data[:50]  # Max 50 rows
            
            if table_data:
                headers = list(table_data[0].keys())
                table_rows = [headers] + [[str(row.get(col, "")) for col in headers] for row in table_data]
                
                table = Table(table_rows)
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    async def _generate_excel_report(self, report_data: Dict[str, Any], request: ReportRequest) -> bytes:
        """Generate secure Excel report"""
        
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            # Summary sheet
            summary_df = pd.DataFrame([report_data.get("summary", {})])
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            
            # Data sheet
            detailed_data = report_data.get("detailed_data", [])
            if detailed_data:
                data_df = pd.DataFrame(detailed_data)
                data_df.to_excel(writer, sheet_name="Data", index=False)
            
            # Metadata sheet
            metadata = {
                "Generated": datetime.now(timezone.utc).isoformat(),
                "Requested_By": request.requested_by,
                "Security_Level": request.security_level.value,
                "Report_ID": request.request_id
            }
            
            if request.requested_by == "rickroll187":
                metadata.update({
                    "Legendary_Status": "🎸 MAXIMUM 🎸",
                    "Swiss_Precision": "⚡ ENABLED ⚡",
                    "Code_Bro_Energy": "💪 INFINITE 💪"
                })
            
            metadata_df = pd.DataFrame([metadata])
            metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    async def _encrypt_report(self, report_data: bytes, access_token: str) -> bytes:
        """Encrypt report with ultra-strong encryption"""
        
        # Generate encryption key from access token
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=access_token[:16].encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(access_token.encode()))
        cipher_suite = Fernet(key)
        
        # Encrypt the report data
        encrypted_data = cipher_suite.encrypt(report_data)
        
        return encrypted_data
    
    async def _check_rate_limit(self, user_id: str) -> bool:
        """Check rate limiting for report generation"""
        
        # Implementation would check Redis for user's recent report requests
        # For now, return True (implement based on your rate limiting system)
        return True

class SecurityError(Exception):
    """Custom security exception"""
    pass

# Global secure reporting system instance
legendary_secure_reporting = None

def get_legendary_secure_reporting(db_session: Session) -> LegendarySecureReportingSystem:
    """Get legendary secure reporting system instance"""
    global legendary_secure_reporting
    if legendary_secure_reporting is None:
        legendary_secure_reporting = LegendarySecureReportingSystem(db_session)
    return legendary_secure_reporting
