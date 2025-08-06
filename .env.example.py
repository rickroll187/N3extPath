# File: .env.example
# 🌍🎸 N3EXTPATH - LEGENDARY ENVIRONMENT VARIABLES TEMPLATE 🎸🌍
# Professional environment configuration template with Swiss precision
# Built: 2025-08-05 19:06:13 UTC by RICKROLL187
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

# =====================================
# 🎸 LEGENDARY FOUNDER CONFIGURATION 🎸
# =====================================
LEGENDARY_FOUNDER=rickroll187
LEGENDARY_MODE=true
SWISS_PRECISION=true
CODE_BRO_ENERGY=maximum
RICKROLL187_ADMIN_MODE=true
LEGENDARY_FEATURES_ENABLED=true

# =====================================
# 🚀 APPLICATION CONFIGURATION 🚀
# =====================================
APP_NAME=N3EXTPATH HR Platform
APP_VERSION=1.0.0
APP_DESCRIPTION=🎸 Legendary HR Platform built by RICKROLL187 🎸
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000
WORKERS=4
RELOAD=false

# =====================================
# 🗄️ DATABASE CONFIGURATION 🗄️
# =====================================
# Primary Database (PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/n3extpath_hr
ASYNC_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/n3extpath_hr

# Database Settings
DATABASE_ECHO=false
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Test Database
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/n3extpath_hr_test

# =====================================
# 🔴 REDIS CONFIGURATION 🔴
# =====================================
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password_here
REDIS_SSL=false
REDIS_POOL_SIZE=50

# =====================================
# 🔐 SECURITY & JWT CONFIGURATION 🔐
# =====================================
# JWT Settings
JWT_SECRET_KEY=your_super_secret_jwt_key_change_this_in_production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# General Security
SECRET_KEY=your_super_secret_key_change_this_in_production

# CORS Settings
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_ALLOW_HEADERS=*

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# =====================================
# 📧 EMAIL CONFIGURATION 📧
# =====================================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_email_password_or_app_password
SMTP_USE_TLS=true
EMAIL_FROM=noreply@n3extpath.com

# =====================================
# ☁️ AWS CONFIGURATION ☁️
# =====================================
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-west-2
AWS_S3_BUCKET=n3extpath-hr-files

# =====================================
# 🔍 MONITORING & LOGGING 🔍
# =====================================
# Sentry for error tracking
SENTRY_DSN=https://your_sentry_dsn@sentry.io/project_id

# Prometheus monitoring
PROMETHEUS_ENABLED=true

# Health checks
HEALTH_CHECK_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/n3extpath.log

# =====================================
# 💾 CACHE CONFIGURATION 💾
# =====================================
CACHE_TTL_DEFAULT=3600
CACHE_TTL_USER_SESSION=1800
CACHE_TTL_PERFORMANCE_DATA=7200

# =====================================
# 📁 FILE UPLOAD CONFIGURATION 📁
# =====================================
MAX_FILE_SIZE=52428800
ALLOWED_FILE_TYPES=.pdf,.doc,.docx,.jpg,.png,.xlsx,.csv
UPLOAD_DIR=uploads

# =====================================
# 🔔 NOTIFICATION CONFIGURATION 🔔
# =====================================
NOTIFICATION_BATCH_SIZE=100
NOTIFICATION_RETRY_ATTEMPTS=3
NOTIFICATION_QUEUE_NAME=notifications

# =====================================
# 📊 PERFORMANCE CONFIGURATION 📊
# =====================================
PERFORMANCE_METRICS_ENABLED=true
PERFORMANCE_ALERT_THRESHOLD=2.0
QUERY_TIMEOUT=30

# =====================================
# 🎸 LEGENDARY FEATURE FLAGS 🎸
# =====================================
SWISS_PRECISION_MODE=true
CODE_BRO_JOKES_ENABLED=true

# =====================================
# 🤖 AI/ML CONFIGURATION 🤖
# =====================================
AI_MODEL_ENABLED=true
ML_MODEL_PATH=models/
AI_CONFIDENCE_THRESHOLD=0.8

# OpenAI API (if using)
OPENAI_API_KEY=your_openai_api_key_here

# =====================================
# 🧪 TESTING CONFIGURATION 🧪
# =====================================
TESTING=false

# =====================================
# 📱 MOBILE & WEBSOCKET CONFIGURATION 📱
# =====================================
# WebSocket settings
WS_URL=ws://localhost:8000/ws

# Push notifications
FCM_SERVER_KEY=your_firebase_server_key
FCM_SENDER_ID=your_firebase_sender_id

# =====================================
# 🐳 DOCKER & DEPLOYMENT 🐳
# =====================================
# Docker settings
DOCKER_REGISTRY=your_docker_registry
DOCKER_IMAGE_TAG=latest

# Kubernetes namespace
K8S_NAMESPACE=n3extpath-hr

# =====================================
# 🎸 LEGENDARY SWISS PRECISION SETTINGS 🎸
# =====================================
# Special settings for RICKROLL187's legendary features
LEGENDARY_API_RATE_MULTIPLIER=5.0
SWISS_PRECISION_LEVEL=maximum
CODE_BRO_ENERGY_LEVEL=infinite
LEGENDARY_CACHE_PRIORITY=true
RICKROLL187_BYPASS_LIMITS=true

# =====================================
# 📈 BUSINESS LOGIC CONFIGURATION 📈
# =====================================
# Performance review settings
PERFORMANCE_REVIEW_CYCLE_MONTHS=6
OKR_CYCLE_MONTHS=3
COMPENSATION_REVIEW_CYCLE_MONTHS=12

# Approval workflows
REQUIRE_MANAGER_APPROVAL=true
REQUIRE_HR_APPROVAL=true
AUTO_APPROVE_LEGENDARY_USER=true

# =====================================
# 🌍 INTERNATIONALIZATION 🌍
# =====================================
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,es,fr,de,zh
TIMEZONE=UTC

# =====================================
# 💼 ENTERPRISE FEATURES 💼
# =====================================
# SSO Configuration
ENABLE_SSO=false
SAML_METADATA_URL=https://your-idp.com/metadata
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret

# LDAP Configuration
ENABLE_LDAP=false
LDAP_SERVER=ldap://your-ldap-server.com
LDAP_BASE_DN=dc=company,dc=com

# =====================================
# 🎸 LEGENDARY MOTTO & CREDITS 🎸
# =====================================
# Built with Swiss precision by RICKROLL187
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
# Maximum code bro energy: ENABLED
# Legendary features: ACTIVATED
# Swiss precision mode: MAXIMUM

# =====================================
# 📝 INSTRUCTIONS FOR USE 📝
# =====================================
# 1. Copy this file to .env
# 2. Replace all placeholder values with your actual configuration
# 3. Never commit .env file to version control
# 4. For production, use secure secret management
# 5. Enable legendary mode for RICKROLL187 🎸
# 6. WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
