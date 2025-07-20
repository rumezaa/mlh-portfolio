#!/usr/bin/env bash

set -euo pipefail
BASE_URL="http://localhost:5000/api/timeline_post"

NAME="TestUser$RANDOM"
EMAIL="test${RANDOM}@example.com"
CONTENT="Automated test at $(date +'%Y-%m-%dT%H:%M:%S')"

echo "Posting new timeline entry..."
POST_RESP=$(curl -s -X POST "$BASE_URL" \
  -d "name=$NAME&email=$EMAIL&content=$CONTENT")

echo "POST response: $POST_RESP"
echo

NEW_ID=$(echo "$POST_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Created entry with ID = $NEW_ID"

echo "Fetching all time line posts"
ALL_RESP=$(curl -s "$BASE_URL")

if echo "$ALL_RESP" | grep -q "\id\":%NEW_ID"; then
    echo "Found ID $NEW_ID in GET response"
else
    echo "Did not find ID $NEW_ID in Get RESPONSE"
    exit 1
fi

echo "Deleting entry $NEW_ID..."
DEL_RESP=$(curl -s -X DELETE "$BASE_URL/$NEW_ID")
echo "DELETE response: $DEL_RESP"
echo

ALL_AFTER=$(curl -s "$BASE_URL")
if echo "$ALL_AFTER" | grep -q "\"id\":$NEW_ID"; then
  echo "Entry $NEW_ID still present after delete"
  exit 1
else
  echo "Entry $NEW_ID successfully removed"
fi

echo "All tests passed!"