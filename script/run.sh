#!/bin/bash

# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Redoc: http://localhost:8000/redoc
uvicorn src.statusx.main:app --reload
