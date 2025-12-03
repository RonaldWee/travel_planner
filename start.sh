#!/bin/bash
# Travel Planner - Start Backend and Frontend
# This script starts both the FastAPI backend and Next.js frontend concurrently

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Process IDs
BACKEND_PID=""
FRONTEND_PID=""

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"

    if [ ! -z "$BACKEND_PID" ]; then
        echo -e "${BLUE}Stopping backend (PID: $BACKEND_PID)${NC}"
        kill $BACKEND_PID 2>/dev/null || true
    fi

    if [ ! -z "$FRONTEND_PID" ]; then
        echo -e "${BLUE}Stopping frontend (PID: $FRONTEND_PID)${NC}"
        kill $FRONTEND_PID 2>/dev/null || true
    fi

    echo -e "${GREEN}Services stopped${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Check if ports are available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${RED}Error: Port $port is already in use${NC}"
        exit 1
    fi
}

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}  Travel Planner - Starting Services${NC}"
echo -e "${GREEN}==================================================${NC}\n"

# Check ports
echo -e "${BLUE}Checking ports...${NC}"
check_port 8000
check_port 3000
echo -e "${GREEN}✓ Ports available${NC}\n"

# Check if backend venv exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${RED}Error: Python virtual environment not found at $BACKEND_DIR/venv${NC}"
    echo -e "${YELLOW}Please create it first with: cd backend && python -m venv venv${NC}"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}Warning: node_modules not found. Installing dependencies...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    cd "$SCRIPT_DIR"
fi

# Start Backend
echo -e "${BLUE}Starting FastAPI Backend...${NC}"
cd "$BACKEND_DIR"
source venv/bin/activate
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}  → http://localhost:8000${NC}"
echo -e "${GREEN}  → Logs: backend.log${NC}\n"
cd "$SCRIPT_DIR"

# Wait a bit for backend to start
sleep 2

# Start Frontend
echo -e "${BLUE}Starting Next.js Frontend...${NC}"
cd "$FRONTEND_DIR"
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo -e "${GREEN}  → http://localhost:3000${NC}"
echo -e "${GREEN}  → Logs: frontend.log${NC}\n"
cd "$SCRIPT_DIR"

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 3

# Check if processes are still running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Backend failed to start. Check backend.log for errors${NC}"
    exit 1
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}✗ Frontend failed to start. Check frontend.log for errors${NC}"
    exit 1
fi

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}  Services Running${NC}"
echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}  Backend:  http://localhost:8000${NC}"
echo -e "${GREEN}  Frontend: http://localhost:3000${NC}"
echo -e "${GREEN}  API Docs: http://localhost:8000/docs${NC}"
echo -e "${GREEN}==================================================${NC}"
echo -e "${YELLOW}\nPress Ctrl+C to stop all services${NC}\n"

# Monitor logs
echo -e "${BLUE}Tailing logs (Ctrl+C to stop)...${NC}\n"
tail -f backend.log frontend.log
