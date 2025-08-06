# File: docker/production/Dockerfile
# 🐳🎸 N3EXTPATH - LEGENDARY PRODUCTION DOCKERFILE 🎸🐳
# Professional production container with Swiss precision
# Built: 2025-08-05 21:53:08 UTC by RICKROLL187
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

# =====================================
# 🎸 MULTI-STAGE LEGENDARY BUILD 🎸
# =====================================

# Stage 1: Python dependencies builder
FROM python:3.11-slim-bullseye as python-builder

# Legendary metadata
LABEL maintainer="RICKROLL187 <rickroll187@n3extpath.com>"
LABEL version="1.0.0-legendary"
LABEL description="N3EXTPATH HR Platform - Built with Swiss precision"
LABEL legendary.founder="rickroll187"
LABEL swiss.precision="maximum"
LABEL code.bro.energy="infinite"

# Set legendary environment variables
ENV LEGENDARY_MODE=true
ENV SWISS_PRECISION=maximum
ENV CODE_BRO_ENERGY=infinite
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    cargo \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn uvicorn[standard]

# Stage 2: Node.js frontend builder
FROM node:18-alpine as frontend-builder

# Legendary frontend build environment
ENV NODE_ENV=production
ENV LEGENDARY_MODE=true
ENV REACT_APP_LEGENDARY_MODE=true
ENV REACT_APP_SWISS_PRECISION=true
ENV REACT_APP_CODE_BRO_ENERGY=maximum
ENV GENERATE_SOURCEMAP=false

WORKDIR /frontend

# Copy package files
COPY frontend/package*.json ./
RUN npm ci --only=production --silent

# Copy frontend source and build
COPY frontend/ .
RUN npm run build:legendary && \
    npm prune --production && \
    npm cache clean --force

# Stage 3: Production runtime
FROM python:3.11-slim-bullseye as production

# Legendary production metadata
LABEL stage="production"
LABEL legendary.optimized="true"
LABEL swiss.precision.level="maximum"
LABEL built.by="rickroll187"
LABEL motto="WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN"

# Create legendary user for security
RUN groupadd -r legendary && \
    useradd -r -g legendary -d /app -s /bin/bash legendary && \
    mkdir -p /app /app/logs /app/uploads /app/static && \
    chown -R legendary:legendary /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libssl1.1 \
    curl \
    netcat \
    dumb-init \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=python-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-builder /usr/local/bin /usr/local/bin

# Copy built frontend from frontend-builder
COPY --from=frontend-builder /frontend/build /app/static/

# Set working directory
WORKDIR /app

# Copy application code
COPY backend/ .

# Copy legendary configuration files
COPY docker/production/gunicorn.conf.py .
COPY docker/production/entrypoint.sh .
COPY docker/production/healthcheck.py .

# Set legendary environment variables
ENV LEGENDARY_MODE=true
ENV SWISS_PRECISION=maximum
ENV CODE_BRO_ENERGY=infinite
ENV PYTHONPATH=/app
ENV WORKERS=4
ENV WORKER_CLASS=uvicorn.workers.UvicornWorker
ENV MAX_REQUESTS=1000
ENV MAX_REQUESTS_JITTER=100
ENV TIMEOUT=30
ENV KEEP_ALIVE=5
ENV PRELOAD_APP=true

# Production optimizations
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

# Security and performance settings
ENV FORWARDED_ALLOW_IPS="*"
ENV PROXY_PROTOCOL=true
ENV LOG_LEVEL=info
ENV ACCESS_LOG_FORMAT='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Make entrypoint executable
RUN chmod +x entrypoint.sh && \
    chown -R legendary:legendary /app

# Create legendary startup script
RUN echo '#!/bin/bash\n\
echo "🎸🎸🎸 LEGENDARY N3EXTPATH STARTING! 🎸🎸🎸"\n\
echo "Built with Swiss precision by RICKROLL187!"\n\
echo "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"\n\
echo "Container started at: $(date -u +\"%Y-%m-%d %H:%M:%S UTC\")"\n\
echo "Legendary Mode: $LEGENDARY_MODE"\n\
echo "Swiss Precision: $SWISS_PRECISION"\n\
echo "Code Bro Energy: $CODE_BRO_ENERGY"\n\
echo "🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸"\n\
exec "$@"' > /app/legendary-startup.sh && \
    chmod +x /app/legendary-startup.sh

# Switch to legendary user
USER legendary

# Expose legendary ports
EXPOSE 8000
EXPOSE 8001

# Health check with Swiss precision
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python healthcheck.py || exit 1

# Volume for legendary data persistence
VOLUME ["/app/logs", "/app/uploads"]

# Legendary entrypoint
ENTRYPOINT ["dumb-init", "--", "/app/legendary-startup.sh", "/app/entrypoint.sh"]

# Default command for legendary service
CMD ["gunicorn", "--config", "gunicorn.conf.py", "main:app"]

# =====================================
# 🎸 LEGENDARY BUILD OPTIMIZATIONS 🎸
# =====================================

# Multi-architecture support
# docker buildx build --platform linux/amd64,linux/arm64 -t n3extpath:legendary .

# Build arguments for legendary customization
ARG LEGENDARY_VERSION=1.0.0
ARG SWISS_PRECISION_LEVEL=maximum
ARG CODE_BRO_ENERGY_LEVEL=infinite
ARG RICKROLL187_ADMIN=true

# Set build-time environment variables
ENV LEGENDARY_VERSION=${LEGENDARY_VERSION}
ENV SWISS_PRECISION_LEVEL=${SWISS_PRECISION_LEVEL}
ENV CODE_BRO_ENERGY_LEVEL=${CODE_BRO_ENERGY_LEVEL}
ENV RICKROLL187_ADMIN=${RICKROLL187_ADMIN}

# =====================================
# 🎸 LEGENDARY METADATA & CREDITS 🎸
# =====================================

# Built with Swiss precision by RICKROLL187
# Container optimized for legendary performance
# Multi-stage build for minimal image size
# Security hardened with non-root user
# Health checks with Swiss precision monitoring
# Production-ready with gunicorn + uvicorn workers
# Static file serving for frontend integration
# Logging configured for legendary debugging
# Environment variables for legendary configuration
# Volume mounts for persistent legendary data

# Docker image tags:
# - n3extpath:legendary-latest
# - n3extpath:legendary-1.0.0
# - n3extpath:legendary-swiss-precision
# - n3extpath:legendary-code-bro-energy
# - n3extpath:legendary-rickroll187-edition

# Legendary build command:
# docker build -f docker/production/Dockerfile -t n3extpath:legendary \
#   --build-arg LEGENDARY_VERSION=1.0.0 \
#   --build-arg SWISS_PRECISION_LEVEL=maximum \
#   --build-arg CODE_BRO_ENERGY_LEVEL=infinite \
#   --build-arg RICKROLL187_ADMIN=true \
#   .

# Swiss precision deployment:
# docker run -d --name n3extpath-legendary \
#   -e LEGENDARY_MODE=true \
#   -e SWISS_PRECISION=maximum \
#   -e CODE_BRO_ENERGY=infinite \
#   -p 8000:8000 \
#   -v legendary-logs:/app/logs \
#   -v legendary-uploads:/app/uploads \
#   n3extpath:legendary

# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
