# File: Dockerfile
# N3EXTPATH HR Platform - Docker Container Configuration
# Built: 2025-08-05 15:23:21 UTC by RICKROLL187
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security (legendary security practices!)
RUN useradd --create-home --shell /bin/bash rickroll187
RUN chown -R rickroll187:rickroll187 /app
USER rickroll187

# Expose port
EXPOSE 8000

# Health check (because legendary apps need health checks!)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the legendary application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
