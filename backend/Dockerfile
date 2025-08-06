# File: backend/Dockerfile
# 🎸🎸🎸 N3EXTPATH - LEGENDARY DOCKER CONTAINER 🎸🎸🎸
# Professional containerization with Swiss precision
# Built: 2025-08-06 00:35:01 UTC by RICKROLL187
# Email: letstalktech010@gmail.com
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

# =====================================
# 🚀 BASE IMAGE - PYTHON WITH ALPINE 🚀
# =====================================
FROM python:3.11-slim-bullseye as base

# Set legendary metadata
LABEL maintainer="RICKROLL187 <letstalktech010@gmail.com>"
LABEL description="🎸 N3EXTPATH Legendary Backend with Swiss Precision 🎸"
LABEL version="1.0.0"
LABEL org.opencontainers.image.title="N3EXTPATH Legendary Backend"
LABEL org.opencontainers.image.description="Professional HR Management Platform with Swiss Precision and Code Bro Energy"
LABEL org.opencontainers.image.authors="RICKROLL187 <letstalktech010@gmail.com>"
LABEL org.opencontainers.image.vendor="N3EXTPATH Legendary Platform"
LABEL org.opencontainers.image.licenses="MIT"
LABEL legendary.founder="rickroll187"
LABEL legendary.swiss_precision="maximum"
LABEL legendary.code_bro_energy="infinite"

# =====================================
# 🎸 LEGENDARY ENVIRONMENT SETUP 🎸
# =====================================

# Set environment variables for legendary performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Legendary platform environment
ENV APP_NAME="N3EXTPATH Legendary Backend" \
    APP_VERSION="1.0.0" \
    LEGENDARY_MODE=true \
    SWISS_PRECISION_ENABLED=true \
    CODE_BRO_ENERGY_LEVEL="infinite" \
    FOUNDER_USERNAME="rickroll187" \
    FOUNDER_EMAIL="letstalktech010@gmail.com"

# Set working directory with Swiss precision
WORKDIR /app

# =====================================
# 🔧 SYSTEM DEPENDENCIES 🔧
# =====================================

# Install system dependencies with legendary precision
RUN apt-get update && apt-get install -y \
    # Build essentials for legendary compilation
    build-essential \
    gcc \
    g++ \
    # PostgreSQL client for legendary database connections  
    libpq-dev \
    postgresql-client \
    # SSL/TLS for legendary security
    libssl-dev \
    libffi-dev \
    # Image processing for legendary file handling
    libjpeg-dev \
    libpng-dev \
    # Additional utilities for legendary operations
    curl \
    wget \
    git \
    vim \
    htop \
    # Cleanup for legendary efficiency
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "🎸 System dependencies installed with Swiss precision! 🎸"

# =====================================
# 👤 USER SETUP FOR LEGENDARY SECURITY 👤
# =====================================

# Create legendary user for security
RUN groupadd -r legendary && \
    useradd -r -g legendary -d /app -s /bin/bash legendary && \
    chown -R legendary:legendary /app && \
    echo "👑 Legendary user created with Swiss precision security! 👑"

# =====================================
# 📦 PYTHON DEPENDENCIES 📦
# =====================================

# Copy requirements files for legendary dependency management
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies with legendary precision
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    echo "📦 Production dependencies installed with Swiss precision! 📦"

# Install development dependencies for legendary development
RUN pip install -r requirements-dev.txt && \
    echo "🧪 Development dependencies installed for legendary coding! 🧪"

# =====================================
# 📁 APPLICATION CODE 📁
# =====================================

# Copy application code with legendary care
COPY --chown=legendary:legendary . .

# Create legendary directories
RUN mkdir -p logs uploads temp && \
    chown -R legendary:legendary logs uploads temp && \
    echo "📁 Legendary directories created with Swiss precision! 📁"

# =====================================
# 🎸 LEGENDARY INITIALIZATION 🎸
# =====================================

# Create legendary startup script
RUN cat > /app/legendary_startup.sh << 'EOF'
#!/bin/bash
# 🎸🎸🎸 LEGENDARY STARTUP SCRIPT 🎸🎸🎸
# Built with Swiss precision by RICKROLL187!
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

echo "🎸🎸🎸 STARTING N3EXTPATH LEGENDARY BACKEND! 🎸🎸🎸"
echo "Built with Swiss precision by RICKROLL187!"
echo "Email: letstalktech010@gmail.com"
echo "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"
echo "Starting at: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸"

# Wait for database to be ready with legendary patience
echo "🗄️ Waiting for legendary database connection..."
while ! nc -z ${DATABASE_HOST:-localhost} ${DATABASE_PORT:-5432}; do
  echo "⏳ Waiting for PostgreSQL database..."
  sleep 2
done
echo "✅ Database connection established with Swiss precision!"

# Wait for Redis to be ready
echo "🔄 Waiting for legendary Redis connection..."
while ! nc -z ${REDIS_HOST:-localhost} ${REDIS_PORT:-6379}; do
  echo "⏳ Waiting for Redis cache..."
  sleep 2
done
echo "✅ Redis connection established with legendary speed!"

# Run database migrations with Swiss precision
echo "🗄️ Running legendary database migrations..."
if alembic upgrade head; then
    echo "✅ Database migrations completed with Swiss precision!"
else
    echo "🚨 Database migration failed! Checking if this is first run..."
    echo "🎸 Initializing legendary database schema..."
    alembic stamp head
    echo "✅ Database schema initialized!"
fi

# Seed database if needed
if [ "$SEED_DATABASE" = "true" ]; then
    echo "🌱 Seeding legendary database with RICKROLL187 founder data..."
    python -c "from database.seed_data import run_seed_data; run_seed_data()"
    echo "✅ Database seeded with legendary data!"
fi

# Start the legendary application
echo "🚀 Starting legendary FastAPI application..."
echo "🎸 Swiss Precision Mode: ${SWISS_PRECISION_ENABLED:-true}"
echo "💪 Code Bro Energy Level: ${CODE_BRO_ENERGY_LEVEL:-infinite}"
echo "👑 Founder: ${FOUNDER_USERNAME:-rickroll187}"
echo "📧 Contact: ${FOUNDER_EMAIL:-letstalktech010@gmail.com}"
echo "🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸"

# Execute the main command
exec "$@"
EOF

# Make startup script executable with legendary permissions
RUN chmod +x /app/legendary_startup.sh && \
    chown legendary:legendary /app/legendary_startup.sh && \
    echo "🎸 Legendary startup script created with Swiss precision! 🎸"

# =====================================
# 🔓 SWITCH TO LEGENDARY USER 🔓
# =====================================
USER legendary

# =====================================
# 🌐 EXPOSE LEGENDARY PORTS 🌐
# =====================================
EXPOSE 8000 9090

# =====================================
# 🏥 HEALTH CHECK 🏥
# =====================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# =====================================
# 🎸 LEGENDARY STARTUP COMMAND 🎸
# =====================================
ENTRYPOINT ["/app/legendary_startup.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]
