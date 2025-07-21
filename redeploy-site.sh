#!/bin/bash

# Pull latest changes from GitHub main branch
git fetch && git reset origin/main --hard

# Activate Python virtual environment
source python3-virtualenv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# restart systemd service and show status
sudo systemctl restart myportfolio
sudo systemctl status myportfolio