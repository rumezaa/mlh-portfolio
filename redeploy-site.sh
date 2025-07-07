#!/bin/bash

# Kill all existing tmux sessions (stops old Flask server)
tmux kill-server

# Navigate to your project directory
cd ~/mlh-portfolio || {
    echo "Directory ~/mlh-portfolio not found!"
    exit 1
}

# Pull latest changes from GitHub main branch
git fetch && git reset origin/main --hard

# Activate Python virtual environment
source python3-virtualenv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start a new detached tmux session that launches the Flask server
tmux new-session -d -s flask-app "bash -c 'cd ~/mlh-portfolio && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'"
