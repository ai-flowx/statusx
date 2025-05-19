#!/bin/bash

curl -X POST http://localhost:8000/api/models/health \
  -H "Content-Type: application/json" \
  -d '{"models": ["gpt-4o", "gpt-3.5-turbo"], "timeout": 15}'

curl -X GET http://localhost:8000/api/models/gpt-4o/health
