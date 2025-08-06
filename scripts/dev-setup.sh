#!/bin/bash
# File: scripts/dev-setup.sh
# N3EXTPATH HR Platform - Development Setup Script
# Built: 2025-08-05 15:52:36 UTC by RICKROLL187
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

set -e

echo "🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸"
echo "🎸                                                    🎸"
echo "🎸        N3EXTPATH LEGENDARY DEVELOPMENT SETUP       🎸"
echo "🎸        Built by RICKROLL187 - Legendary Founder    🎸"
echo "🎸        $(date -u '+%Y-%m-%d %H:%M:%S') UTC          🎸"
echo "🎸        WE ARE CODE BROS THE CREATE THE BEST        🎸"
echo "🎸        AND CRACK JOKES TO HAVE FUN!                🎸"
echo "🎸                                                    🎸"
echo "🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸"
echo ""

# Check if required tools are installed
check_requirements() {
    echo "🔍 Checking legendary requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed!"
        exit 1
    fi
    echo "✅ Python $(python3 --version) found"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is not installed!"
        exit 1
    fi
    echo "✅ Node.js $(node --version) found"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is not installed!"
        exit 1
    fi
    echo "✅ npm $(npm --version) found"
    
    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        echo "✅ Docker $(docker --version) found"
    else
        echo "⚠️  Docker not found (optional for development)"
    fi
    
    echo ""
}

# Setup backend
setup_backend() {
    echo "🐍 Setting up legendary backend..."
    
    cd backend/
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "📦 Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install pytest pytest-asyncio httpx  # Test dependencies
    
    echo "✅ Backend setup complete!"
    cd ..
    echo ""
}

# Setup frontend
setup_frontend() {
    echo "⚛️ Setting up legendary frontend..."
    
    cd frontend/
    
    # Install dependencies
    echo "📦 Installing Node.js dependencies..."
    npm install
    
    echo "✅ Frontend setup complete!"
    cd ..
    echo ""
}

# Create development environment file
create_env_file() {
    echo "🔧 Creating development environment file..."
    
    if [ ! -f "backend/.env" ]; then
        cat > backend/.env << EOF
# N3EXTPATH Development Environment
# Built by RICKROLL187 at $(date -u '+%Y-%m-%d %H:%M:%S') UTC
# WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!

APP_NAME="N3EXTPATH HR Platform"
ENVIRONMENT="development"
DEBUG=true
LEGENDARY_MODE=enabled
RICKROLL187_MODE=true

# Development settings
API_HOST=localhost
API_PORT=8000
FRONTEND_URL=http://localhost:3000

# Swiss precision timing
RESPONSE_TIMEOUT=30
REQUEST_TIMEOUT=60

# Code bro settings
CODE_BRO_JOKES=enabled
SWISS_PRECISION=true
LEGENDARY_BRANDING=enabled
EOF
        echo "✅ Created backend/.env file"
    else
        echo "✅ Backend .env file already exists"
    fi
    
    echo ""
}

# Create development scripts
create_dev_scripts() {
    echo "📝 Creating legendary development scripts..."
    
    # Backend start script
    cat > scripts/start-backend.sh << 'EOF'
#!/bin/bash
echo "🐍 Starting legendary backend server..."
cd backend/
source venv/bin/activate
python main.py
EOF
    chmod +x scripts/start-backend.sh
    
    # Frontend start script
    cat > scripts/start-frontend.sh << 'EOF'
#!/bin/bash
echo "⚛️ Starting legendary frontend server..."
cd frontend/
npm run dev
EOF
    chmod +x scripts/start-frontend.sh
    
    # Full stack start script
    cat > scripts/start-fullstack.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting legendary full stack application..."
echo "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"

# Start backend in background
echo "🐍 Starting backend..."
cd backend/
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚛️ Starting frontend..."
cd frontend/
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎸 LEGENDARY N3EXTPATH SERVERS STARTED! 🎸"
echo "🐍 Backend: http://localhost:8000"
echo "⚛️ Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; echo '🛑 Servers stopped!'; exit" INT
wait
EOF
    chmod +x scripts/start-fullstack.sh
    
    # Test script
    cat > scripts/run-tests.sh << 'EOF'
#!/bin/bash
echo "🧪 Running legendary test suite..."
echo "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"

echo "🐍 Running backend tests..."
cd backend/
source venv/bin/activate
python -m pytest test_main.py -v
cd ..

echo "⚛️ Running frontend tests..."
cd frontend/
npm test -- --watchAll=false
cd ..

echo "✅ All legendary tests completed!"
EOF
    chmod +x scripts/run-tests.sh
    
    echo "✅ Development scripts created!"
    echo ""
}

# Main setup function
main() {
    echo "🚀 Starting legendary development setup..."
    echo ""
    
    # Create scripts directory
    mkdir -p scripts/
    
    check_requirements
    setup_backend
    setup_frontend
    create_env_file
    create_dev_scripts
    
    echo "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
    echo "🎉                                                    🎉"
    echo "🎉        LEGENDARY SETUP COMPLETE!                   🎉"
    echo "🎉        N3EXTPATH HR Platform Ready for Development 🎉"
    echo "🎉        Built by RICKROLL187 with Swiss Precision!  🎉"
    echo "🎉                                                    🎉"
    echo "🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉"
    echo ""
    echo "🎸 Quick Start Commands:"
    echo "   ./scripts/start-backend.sh     - Start backend only"
    echo "   ./scripts/start-frontend.sh    - Start frontend only"
    echo "   ./scripts/start-fullstack.sh   - Start both servers"
    echo "   ./scripts/run-tests.sh         - Run all tests"
    echo ""
    echo "🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸"
}

# Run main function
main "$@"
