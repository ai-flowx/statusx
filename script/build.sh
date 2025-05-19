#!/bin/bash

docker build -t craftslab/statusx .
docker run -p 8000:8000 --env-file .env craftslab/statusx
