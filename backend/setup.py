# File: backend/setup.py
"""
🎸🎸🎸 N3EXTPATH - LEGENDARY SETUP CONFIGURATION 🎸🎸🎸
Professional Python package setup with Swiss precision
Built: 2025-08-06 00:30:05 UTC by RICKROLL187
Email: letstalktech010@gmail.com
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

from setuptools import setup, find_packages
from pathlib import Path
import re

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

# Read version from __init__.py
def get_version():
    version_file = this_directory / "__init__.py"
    if version_file.exists():
        version_content = version_file.read_text()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_content, re.M)
        if version_match:
            return version_match.group(1)
    return "1.0.0"

# Read requirements
def parse_requirements(filename):
    requirements_file = this_directory / filename
    if requirements_file.exists():
        with open(requirements_file, 'r') as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-r'):
                    requirements.append(line)
            return requirements
    return []

setup(
    # =====================================
    # 🎸 PACKAGE INFORMATION 🎸
    # =====================================
    name="n3extpath-legendary-backend",
    version=get_version(),
    author="RICKROLL187",
    author_email="letstalktech010@gmail.com",
    description="🎸 Legendary HR Management Platform Backend with Swiss Precision 🎸",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rickroll187/n3extpath-legendary-backend",
    project_urls={
        "Bug Tracker": "https://github.com/rickroll187/n3extpath-legendary-backend/issues",
        "Documentation": "https://n3extpath.legendary/docs",
        "Source Code": "https://github.com/rickroll187/n3extpath-legendary-backend",
        "Founder": "https://letstalktech010@gmail.com"
    },
    
    # =====================================
    # 📦 PACKAGE CONFIGURATION 📦
    # =====================================
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Office/Business :: Human Resources",
    ],
    
    # =====================================
    # 🔧 DEPENDENCIES & REQUIREMENTS 🔧
    # =====================================
    python_requires=">=3.8",
    install_requires=parse_requirements("requirements.txt"),
    extras_require={
        "dev": parse_requirements("requirements-dev.txt"),
        "test": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "httpx>=0.25.2",
            "faker>=20.1.0"
        ],
        "docs": [
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.5.2",
            "sphinx>=7.2.6"
        ],
        "production": [
            "gunicorn>=21.2.0",
            "uvicorn[standard]>=0.24.0",
            "sentry-sdk[fastapi]>=1.38.0"
        ]
    },
    
    # =====================================
    # 📝 ENTRY POINTS & SCRIPTS 📝
    # =====================================
    entry_points={
        "console_scripts": [
            "n3extpath-server=main:app",
            "n3extpath-migrate=database.migrations.env:run_migrations_online",
            "n3extpath-seed=database.seed_data:run_seed_data",
        ],
    },
    
    # =====================================
    # 📁 PACKAGE DATA 📁
    # =====================================
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json", "*.ini"],
        "database": ["migrations/versions/*.py", "migrations/*.py"],
        "config": ["*.yml", "*.yaml", "*.json"],
    },
    
    # =====================================
    # 🎸 LEGENDARY METADATA 🎸
    # =====================================
    keywords=[
        "hr-management", "performance-reviews", "okr", "team-management",
        "fastapi", "sqlalchemy", "postgresql", "legendary", "swiss-precision",
        "code-bro-energy", "rickroll187", "n3extpath"
    ],
    
    # License
    license="MIT",
    
    # Additional metadata
    zip_safe=False,
    platforms=["any"],
    
    # Custom metadata for legendary features
    options={
        "bdist_wheel": {
            "universal": "0"
        }
    }
)
