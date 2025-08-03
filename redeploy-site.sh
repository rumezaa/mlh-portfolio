#!/bin/bash
cd /root/mlh-portfolio

# Pull latest changes from GitHub main branch
git fetch && git reset origin/main --hard

# 3) Tear down any running containers
docker compose -f docker-compose.prod.yml down

# 4) Rebuild images & bring everything up in detached mode
docker compose -f docker-compose.prod.yml up -d --build