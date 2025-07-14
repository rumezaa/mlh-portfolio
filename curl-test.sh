#!/bin/bash

POST_RESPONSE=$(curl -X POST http://127.0.0.1:5000/api/timeline_post -d 'name=Test&email=test@example.com&content=This was a post request!')

echo "POST response:"
echo "$POST_RESPONSE"

GET_RESPONSE=$(curl http://127.0.0.1:5000/api/timeline_post)

echo "GET response:"
echo "$GET_RESPONSE" | jq .

echo "Checking if the new post exists..."

FOUND=$(echo "$GET_RESPONSE" | jq -e \
  '.timeline_posts[] | select(.name=="Test" and .email=="test@example.com" and .content=="This was a post request!")')

if [ $? -eq 0 ]; then
  echo "POST was successful "
  echo "$FOUND"

  DELETE_RESPONSE=$(curl -X DELETE http://127.0.0.1:5000/api/timeline_post \
    -d 'name=Test&email=test@example.com&content=This was a post request!')

  echo "DELETE response:"
  echo "$DELETE_RESPONSE"
else
  echo "POST was unsuccessful"
fi

