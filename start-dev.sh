#!/bin/bash
# Simple dev start script - runs both services in foreground with live output

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}Starting Travel Planner Development Servers${NC}\n"

# Function to run backend
run_backend() {
    echo -e "${BLUE}[BACKEND] Starting on http://localhost:8000${NC}"
    cd "$SCRIPT_DIR/backend"
    source venv/bin/activate
    python main.py 2>&1 | sed 's/^/[BACKEND] /'
}

# Function to run frontend
run_frontend() {
    echo -e "${BLUE}[FRONTEND] Starting on http://localhost:3000${NC}"
    cd "$SCRIPT_DIR/frontend"
    npm run dev 2>&1 | sed 's/^/[FRONTEND] /'
}

# Run both in parallel
run_backend & run_frontend &

# Wait for both processes
wait
