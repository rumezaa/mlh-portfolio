#!/bin/bash

tmux kill-server
cd mlh-portfolio  

git fetch
git reset origin/main --hard

source venv/bin/activate
pip install -r requirements.txt

tmux new -d "source venv/bin/activate && flask run --host=0.0.0.0"

