#!/bin/bash
# Start only the frontend server

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}Starting Travel Planner Frontend${NC}"
echo -e "${BLUE}→ http://localhost:3000${NC}\n"

cd "$SCRIPT_DIR/frontend"
npm run dev
