#!/bin/bash

## Pass URL
URL="http://tets-example.com"

## Get response code for Http 
HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$URL")

# Check if the response code is 301 or 302 (redirect)
if [ "$HTTP" -eq "301" ] || [ "$HTTP" -eq "302" ]; then
  echo " redirection test PASSED."
else
  echo "redirection test FAILED."
fi
