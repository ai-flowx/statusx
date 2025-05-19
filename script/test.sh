#!/bin/bash

curl -X POST http://localhost:8000/models/health \
  -H "Content-Type: application/json" \
  -d '{"models": ["gpt-4o", "gpt-3.5-turbo"], "timeout": 15}'

curl -X GET http://localhost:8000/models/gpt-4o/health
