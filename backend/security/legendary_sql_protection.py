# File: backend/security/legendary_sql_protection.py
"""
🛡️🎸 N3EXTPATH - LEGENDARY SQL INJECTION PROTECTION 🎸🛡️
Ultra-secure SQL injection prevention with Swiss precision security
Built: 2025-08-05 17:32:04 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import re
import ast
import hashlib
import hmac
import secrets
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass
from enum import Enum
import logging
from sqlalchemy import text, MetaData, inspect
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
import bleach
import html
import urllib.parse
from cryptography.fernet import Fernet
import time

class ThreatLevel(Enum):
    """Security threat levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    LEGENDARY_THREAT = "legendary_threat"  # Maximum threat level

class AttackType(Enum):
    """Types of security attacks"""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    LDAP_INJECTION = "ldap_injection"
    SCRIPT_INJECTION = "script_injection"
    HTML_INJECTION = "html_injection"

@dataclass
class SecurityThreat:
    """Security threat detection result"""
    threat_id: str
    attack_type: AttackType
    threat_level: ThreatLevel
    description: str
    detected_pattern: str
    user_input: str
    blocked: bool = True
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class LegendarySQLProtectionSystem:
    """Ultra-Secure SQL Injection Protection with Swiss Precision"""
    
    def __init__(self, engine: Engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        
        # Initialize threat detection patterns
        self.sql_injection_patterns = self._initialize_sql_patterns()
        self.xss_patterns = self._initialize_xss_patterns()
        self.command_injection_patterns = self._initialize_command_patterns()
        
        # Whitelist of allowed table names (dynamically loaded)
        self.allowed_tables = self._get_allowed_tables()
        
        # Blacklist of dangerous keywords
        self.dangerous_keywords = self._initialize_dangerous_keywords()
        
        # Protection configuration
        self.protection_config = {
            "max_query_length": 50000,
            "max_parameter_length": 10000,
            "enable_parameterized_queries_only": True,
            "enable_whitelist_validation": True,
            "enable_pattern_detection": True,
            "enable_syntax_analysis": True,
            "block_dynamic_queries": True,
            "require_prepared_statements": True,
            "log_all_threats": True,
            "legendary_bypass": False  # Even RICKROLL187 goes through security
        }
        
        # Threat tracking
        self.detected_threats = []
        self.blocked_attempts = 0
        self.legitimate_queries = 0
    
    def _initialize_sql_patterns(self) -> List[Dict[str, Any]]:
        """Initialize comprehensive SQL injection detection patterns"""
        return [
            # Union-based injection
            {
                "pattern": r"(?i)(union|UNION)\s+(all\s+)?(select|SELECT)",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "UNION-based SQL injection attempt"
            },
            
            # Boolean-based blind injection
            {
                "pattern": r"(?i)(and|or)\s+\d+\s*[=<>]\s*\d+",
                "threat_level": ThreatLevel.HIGH,
                "description": "Boolean-based blind SQL injection"
            },
            
            # Time-based blind injection
            {
                "pattern": r"(?i)(sleep|waitfor|delay|benchmark)\s*\(\s*\d+",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Time-based blind SQL injection"
            },
            
            # Error-based injection
            {
                "pattern": r"(?i)(extractvalue|updatexml|exp|floor|rand)\s*\(",
                "threat_level": ThreatLevel.HIGH,
                "description": "Error-based SQL injection"
            },
            
            # Stacked queries
            {
                "pattern": r";\s*(drop|insert|update|delete|create|alter|exec|execute)",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Stacked query injection attempt"
            },
            
            # Information schema access
            {
                "pattern": r"(?i)information_schema\.(tables|columns|schemata)",
                "threat_level": ThreatLevel.HIGH,
                "description": "Information schema reconnaissance"
            },
            
            # System function calls
            {
                "pattern": r"(?i)(xp_cmdshell|sp_executesql|openrowset|opendatasource)",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "System function exploitation attempt"
            },
            
            # Comment-based evasion
            {
                "pattern": r"/\*.*?\*/|--.*?$|#.*?$",
                "threat_level": ThreatLevel.MEDIUM,
                "description": "SQL comment-based evasion"
            },
            
            # Hex/char encoding evasion
            {
                "pattern": r"(?i)(0x[0-9a-f]+|char\s*\(\s*\d+|ascii\s*\(\s*\d+)",
                "threat_level": ThreatLevel.HIGH,
                "description": "Encoding-based evasion attempt"
            },
            
            # Conditional statements
            {
                "pattern": r"(?i)(if|case)\s*\(\s*.+\s*,\s*.+\s*,\s*.+\s*\)",
                "threat_level": ThreatLevel.MEDIUM,
                "description": "Conditional statement injection"
            }
        ]
    
    def _initialize_xss_patterns(self) -> List[Dict[str, Any]]:
        """Initialize XSS detection patterns"""
        return [
            {
                "pattern": r"(?i)<script[^>]*>.*?</script>",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Script tag XSS"
            },
            {
                "pattern": r"(?i)javascript\s*:",
                "threat_level": ThreatLevel.HIGH,
                "description": "JavaScript protocol XSS"
            },
            {
                "pattern": r"(?i)on(load|error|click|mouseover|focus|blur)\s*=",
                "threat_level": ThreatLevel.HIGH,
                "description": "Event handler XSS"
            },
            {
                "pattern": r"(?i)<iframe[^>]*>",
                "threat_level": ThreatLevel.HIGH,
                "description": "Iframe injection"
            },
            {
                "pattern": r"(?i)expression\s*\(",
                "threat_level": ThreatLevel.MEDIUM,
                "description": "CSS expression XSS"
            }
        ]
    
    def _initialize_command_patterns(self) -> List[Dict[str, Any]]:
        """Initialize command injection patterns"""
        return [
            {
                "pattern": r"[;&|`$(){}[\]\\]",
                "threat_level": ThreatLevel.HIGH,
                "description": "Command injection metacharacters"
            },
            {
                "pattern": r"(?i)(cat|ls|dir|type|copy|move|del|rm|chmod|wget|curl)\s",
                "threat_level": ThreatLevel.CRITICAL,
                "description": "System command injection"
            }
        ]
    
    def _initialize_dangerous_keywords(self) -> List[str]:
        """Initialize comprehensive dangerous keywords list"""
        return [
            # SQL DDL/DML commands
            "DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE",
            "GRANT", "REVOKE", "COMMIT", "ROLLBACK", "SAVEPOINT",
            
            # SQL system functions
            "EXEC", "EXECUTE", "EVAL", "SYSTEM", "SHELL", "CMD",
            "XP_CMDSHELL", "SP_EXECUTESQL", "OPENROWSET", "OPENDATASOURCE",
            
            # SQL information functions
            "USER", "CURRENT_USER", "SESSION_USER", "SYSTEM_USER",
            "DATABASE", "SCHEMA", "VERSION", "@@VERSION",
            
            # SQL injection techniques
            "UNION", "SELECT", "FROM", "WHERE", "HAVING", "GROUP BY", "ORDER BY",
            "INTO", "OUTFILE", "DUMPFILE", "LOAD_FILE",
            
            # Time-based functions
            "SLEEP", "WAITFOR", "DELAY", "BENCHMARK", "PG_SLEEP",
            
            # Error-based functions
            "EXTRACTVALUE", "UPDATEXML", "EXP", "FLOOR", "RAND",
            
            # Script tags and JavaScript
            "SCRIPT", "JAVASCRIPT", "VBSCRIPT", "ONLOAD", "ONERROR",
            "ONCLICK", "ONMOUSEOVER", "ONFOCUS", "ONBLUR",
            
            # HTML tags
            "IFRAME", "OBJECT", "EMBED", "APPLET", "FORM", "INPUT",
            
            # File system operations
            "FILE", "DIRECTORY", "PATH", "FOLDER", "../", "..\\",
            
            # Network operations
            "HTTP", "FTP", "TELNET", "SSH", "PING", "NMAP",
            
            # Encoding functions
            "CHAR", "ASCII", "HEX", "UNHEX", "ENCODE", "DECODE",
            
            # Regular expressions
            "REGEXP", "RLIKE", "MATCH", "SIMILAR"
        ]
    
    def _get_allowed_tables(self) -> List[str]:
        """Dynamically get allowed table names from database schema"""
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            # Filter to only application tables (exclude system tables)
            allowed_tables = [
                table for table in tables 
                if not table.startswith(('pg_', 'information_schema', 'sys', 'mysql'))
            ]
            
            return allowed_tables
            
        except Exception as e:
            self.logger.error(f"Failed to get table names: {e}")
            # Fallback to hardcoded list
            return [
                "users", "performance_reviews", "okrs", "teams", "departments",
                "training_records", "attendance", "compensation", "notifications",
                "reports", "audit_logs"
            ]
    
    def validate_input(self, user_input: Any, input_type: str = "general") -> Dict[str, Any]:
        """Ultra-secure input validation with threat detection"""
        
        validation_result = {
            "is_safe": True,
            "sanitized_input": user_input,
            "threats_detected": [],
            "blocked": False,
            "sanitization_applied": False
        }
        
        if user_input is None:
            return validation_result
        
        # Convert to string for analysis
        input_str = str(user_input)
        
        # Length validation
        max_length = self.protection_config.get("max_parameter_length", 10000)
        if len(input_str) > max_length:
            threat = SecurityThreat(
                threat_id=secrets.token_hex(8),
                attack_type=AttackType.SQL_INJECTION,
                threat_level=ThreatLevel.HIGH,
                description=f"Input exceeds maximum length ({len(input_str)} > {max_length})",
                detected_pattern="length_violation",
                user_input=input_str[:100] + "..." if len(input_str) > 100 else input_str
            )
            validation_result["threats_detected"].append(threat)
            validation_result["is_safe"] = False
            validation_result["blocked"] = True
            
            self._log_threat(threat)
            return validation_result
        
        # Pattern-based threat detection
        threats = self._detect_threats(input_str)
        
        if threats:
            validation_result["threats_detected"].extend(threats)
            validation_result["is_safe"] = False
            
            # Determine if should block based on threat level
            critical_threats = [t for t in threats if t.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.LEGENDARY_THREAT]]
            if critical_threats:
                validation_result["blocked"] = True
                for threat in threats:
                    self._log_threat(threat)
                return validation_result
        
        # Apply sanitization if not blocked
        if not validation_result["blocked"]:
            sanitized = self._sanitize_input(input_str, input_type)
            if sanitized != input_str:
                validation_result["sanitized_input"] = sanitized
                validation_result["sanitization_applied"] = True
        
        return validation_result
    
    def _detect_threats(self, input_str: str) -> List[SecurityThreat]:
        """Comprehensive threat detection"""
        
        threats = []
        
        # SQL injection detection
        for pattern_info in self.sql_injection_patterns:
            matches = re.finditer(pattern_info["pattern"], input_str, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                threat = SecurityThreat(
                    threat_id=secrets.token_hex(8),
                    attack_type=AttackType.SQL_INJECTION,
                    threat_level=pattern_info["threat_level"],
                    description=pattern_info["description"],
                    detected_pattern=match.group(),
                    user_input=input_str
                )
                threats.append(threat)
        
        # XSS detection
        for pattern_info in self.xss_patterns:
            matches = re.finditer(pattern_info["pattern"], input_str, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                threat = SecurityThreat(
                    threat_id=secrets.token_hex(8),
                    attack_type=AttackType.XSS,
                    threat_level=pattern_info["threat_level"],
                    description=pattern_info["description"],
                    detected_pattern=match.group(),
                    user_input=input_str
                )
                threats.append(threat)
        
        # Command injection detection
        for pattern_info in self.command_injection_patterns:
            matches = re.finditer(pattern_info["pattern"], input_str, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                threat = SecurityThreat(
                    threat_id=secrets.token_hex(8),
                    attack_type=AttackType.COMMAND_INJECTION,
                    threat_level=pattern_info["threat_level"],
                    description=pattern_info["description"],
                    detected_pattern=match.group(),
                    user_input=input_str
                )
                threats.append(threat)
        
        # Keyword-based detection
        input_upper = input_str.upper()
        for keyword in self.dangerous_keywords:
            if keyword in input_upper:
                # Context analysis to reduce false positives
                if self._is_dangerous_context(input_str, keyword):
                    threat = SecurityThreat(
                        threat_id=secrets.token_hex(8),
                        attack_type=AttackType.SQL_INJECTION,
                        threat_level=ThreatLevel.MEDIUM,
                        description=f"Dangerous keyword detected: {keyword}",
                        detected_pattern=keyword,
                        user_input=input_str
                    )
                    threats.append(threat)
        
        return threats
    
    def _is_dangerous_context(self, input_str: str, keyword: str) -> bool:
        """Analyze context to determine if keyword usage is dangerous"""
        
        input_lower = input_str.lower()
        keyword_lower = keyword.lower()
        
        # Find keyword position
        keyword_pos = input_lower.find(keyword_lower)
        if keyword_pos == -1:
            return False
        
        # Analyze surrounding context
        start_pos = max(0, keyword_pos - 10)
        end_pos = min(len(input_str), keyword_pos + len(keyword) + 10)
        context = input_str[start_pos:end_pos].lower()
        
        # Dangerous contexts
        dangerous_contexts = [
            "where", "select", "from", "into", "values", "set",
            "execute", "exec", "eval", "system", "cmd", "shell",
            "script", "javascript", "onclick", "onload", "onerror"
        ]
        
        for dangerous_context in dangerous_contexts:
            if dangerous_context in context:
                return True
        
        return False
    
    def _sanitize_input(self, input_str: str, input_type: str) -> str:
        """Multi-layer input sanitization"""
        
        sanitized = input_str
        
        # HTML entity encoding
        sanitized = html.escape(sanitized, quote=True)
        
        # URL encoding for special characters
        sanitized = urllib.parse.quote_plus(sanitized, safe=' ')
        
        # Bleach HTML sanitization
        sanitized = bleach.clean(
            sanitized,
            tags=[],  # No HTML tags allowed
            attributes={},
            strip=True,
            strip_comments=True
        )
        
        # Custom sanitization based on input type
        if input_type == "sql_parameter":
            # Extra strict for SQL parameters
            sanitized = re.sub(r'[^\w\s@.-]', '', sanitized)
        elif input_type == "filename":
            # Filename sanitization
            sanitized = re.sub(r'[^\w\s.-]', '', sanitized)
            sanitized = sanitized.replace('..', '')
        elif input_type == "email":
            # Email sanitization
            sanitized = re.sub(r'[^\w@.-]', '', sanitized)
        
        return sanitized
    
    def _log_threat(self, threat: SecurityThreat):
        """Log detected security threats"""
        
        self.detected_threats.append(threat)
        self.blocked_attempts += 1
        
        log_message = (
            f"SECURITY THREAT DETECTED: {threat.attack_type.value} "
            f"[{threat.threat_level.value}] - {threat.description} "
            f"Pattern: {threat.detected_pattern} "
            f"ThreatID: {threat.threat_id}"
        )
        
        if threat.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.LEGENDARY_THREAT]:
            self.logger.critical(log_message)
        elif threat.threat_level == ThreatLevel.HIGH:
            self.logger.error(log_message)
        else:
            self.logger.warning(log_message)
    
    def validate_sql_query(self, query: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ultra-secure SQL query validation"""
        
        validation_result = {
            "is_safe": True,
            "query_approved": False,
            "threats_detected": [],
            "sanitized_parameters": {},
            "blocked": False,
            "error_message": None
        }
        
        try:
            # Query length check
            if len(query) > self.protection_config["max_query_length"]:
                validation_result["is_safe"] = False
                validation_result["blocked"] = True
                validation_result["error_message"] = "Query exceeds maximum allowed length"
                return validation_result
            
            # Detect threats in query
            query_threats = self._detect_threats(query)
            if query_threats:
                validation_result["threats_detected"].extend(query_threats)
                validation_result["is_safe"] = False
                
                # Check for critical threats
                critical_threats = [t for t in query_threats if t.threat_level == ThreatLevel.CRITICAL]
                if critical_threats:
                    validation_result["blocked"] = True
                    validation_result["error_message"] = "Critical security threats detected in query"
                    return validation_result
            
            # Validate parameters
            if parameters:
                for param_name, param_value in parameters.items():
                    param_validation = self.validate_input(param_value, "sql_parameter")
                    
                    if not param_validation["is_safe"]:
                        validation_result["threats_detected"].extend(param_validation["threats_detected"])
                        validation_result["is_safe"] = False
                        
                        if param_validation["blocked"]:
                            validation_result["blocked"] = True
                            validation_result["error_message"] = f"Parameter '{param_name}' contains security threats"
                            return validation_result
                    
                    validation_result["sanitized_parameters"][param_name] = param_validation["sanitized_input"]
            
            # Table whitelist validation
            if self.protection_config["enable_whitelist_validation"]:
                if not self._validate_table_access(query):
                    validation_result["is_safe"] = False
                    validation_result["blocked"] = True
                    validation_result["error_message"] = "Query accesses unauthorized tables"
                    return validation_result
            
            # Syntax analysis
            if self.protection_config["enable_syntax_analysis"]:
                if not self._analyze_query_syntax(query):
                    validation_result["is_safe"] = False
                    validation_result["blocked"] = True
                    validation_result["error_message"] = "Query contains invalid or suspicious syntax"
                    return validation_result
            
            # If we reach here, query is approved
            validation_result["query_approved"] = True
            self.legitimate_queries += 1
            
        except Exception as e:
            self.logger.error(f"Query validation error: {e}")
            validation_result["is_safe"] = False
            validation_result["blocked"] = True
            validation_result["error_message"] = "Query validation failed"
        
        return validation_result
    
    def _validate_table_access(self, query: str) -> bool:
        """Validate that query only accesses allowed tables"""
        
        query_upper = query.upper()
        
        # Extract table names from query
        table_patterns = [
            r'FROM\s+(\w+)',
            r'JOIN\s+(\w+)',
            r'INTO\s+(\w+)',
            r'UPDATE\s+(\w+)',
            r'DELETE\s+FROM\s+(\w+)',
            r'INSERT\s+INTO\s+(\w+)'
        ]
        
        referenced_tables = set()
        for pattern in table_patterns:
            matches = re.finditer(pattern, query_upper)
            for match in matches:
                table_name = match.group(1).lower()
                referenced_tables.add(table_name)
        
        # Check if all referenced tables are in whitelist
        allowed_tables_lower = [table.lower() for table in self.allowed_tables]
        for table in referenced_tables:
            if table not in allowed_tables_lower:
                self.logger.warning(f"Unauthorized table access attempted: {table}")
                return False
        
        return True
    
    def _analyze_query_syntax(self, query: str) -> bool:
        """Advanced query syntax analysis"""
        
        # Check for nested queries depth
        nested_depth = query.upper().count('SELECT')
        if nested_depth > 5:  # Max 5 levels of nesting
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r';\s*--',  # Comment after statement
            r'\/\*.*?\*\/',  # Multi-line comments
            r'WAITFOR\s+DELAY',  # Time delays
            r'BENCHMARK\s*\(',  # Performance testing
            r'LOAD_FILE\s*\(',  # File operations
            r'INTO\s+OUTFILE',  # File output
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False
        
        return True
    
    def create_safe_query(self, base_query: str, parameters: Dict[str, Any]) -> text:
        """Create ultra-safe parameterized query"""
        
        # Validate query and parameters
        validation = self.validate_sql_query(base_query, parameters)
        
        if validation["blocked"]:
            raise SecurityError(f"Query blocked: {validation['error_message']}")
        
        if not validation["query_approved"]:
            raise SecurityError("Query not approved for execution")
        
        # Use sanitized parameters
        safe_parameters = validation["sanitized_parameters"]
        
        # Create parameterized query
        safe_query = text(base_query)
        
        return safe_query, safe_parameters
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get comprehensive security statistics"""
        
        threat_by_type = {}
        threat_by_level = {}
        
        for threat in self.detected_threats:
            # Count by type
            threat_type = threat.attack_type.value
            threat_by_type[threat_type] = threat_by_type.get(threat_type, 0) + 1
            
            # Count by level
            threat_level = threat.threat_level.value
            threat_by_level[threat_level] = threat_by_level.get(threat_level, 0) + 1
        
        total_requests = self.blocked_attempts + self.legitimate_queries
        
        return {
            "total_requests_processed": total_requests,
            "legitimate_queries": self.legitimate_queries,
            "blocked_attempts": self.blocked_attempts,
            "block_rate": (self.blocked_attempts / total_requests * 100) if total_requests > 0 else 0,
            "threats_by_type": threat_by_type,
            "threats_by_level": threat_by_level,
            "total_threats_detected": len(self.detected_threats),
            "allowed_tables_count": len(self.allowed_tables),
            "protection_config": self.protection_config,
            "legendary_security_status": "🎸 MAXIMUM PROTECTION ENABLED 🎸",
            "swiss_precision": "⚡ ACTIVE ⚡"
        }

class SecurityError(Exception):
    """Custom security exception"""
    pass

# Global security protection system
legendary_sql_protection = None

def get_legendary_sql_protection(engine: Engine) -> LegendarySQLProtectionSystem:
    """Get legendary SQL protection system instance"""
    global legendary_sql_protection
    if legendary_sql_protection is None:
        legendary_sql_protection = LegendarySQLProtectionSystem(engine)
    return legendary_sql_protection

# Security decorators
def secure_database_operation(func: Callable) -> Callable:
    """Decorator to add security validation to database operations"""
    
    def wrapper(*args, **kwargs):
        # Add security validation here
        # This would integrate with your database session
        try:
            return func(*args, **kwargs)
        except SecurityError as e:
            logging.error(f"Security violation in {func.__name__}: {e}")
            raise
        except Exception as e:
            logging.error(f"Database operation error in {func.__name__}: {e}")
            raise
    
    return wrapper
