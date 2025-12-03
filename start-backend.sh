#!/bin/bash
# Start only the backend server

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}Starting Travel Planner Backend${NC}"
echo -e "${BLUE}→ http://localhost:8000${NC}"
echo -e "${BLUE}→ API Docs: http://localhost:8000/docs${NC}\n"

cd "$SCRIPT_DIR/backend"
source venv/bin/activate
python main.py
