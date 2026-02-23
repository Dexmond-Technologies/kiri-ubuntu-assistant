#!/bin/bash

# Absolute project path
PROJECT_DIR="$HOME/Documents/Dexmond_Technologies/kiri"

# Move to project directory
cd "$PROJECT_DIR" || {
    echo "Project directory not found"
    exit 1
}

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "venv not found"
    exit 1
fi

# Optional: install requirements if first run
# pip install -r REQUIREMENTS.md 2>/dev/null

# Run assistant
python3 kiri.py

# Deactivate after exit
deactivate
