#!/bin/bash

if [ "$NVIDIA_RUNTIME" = "true" ]; then
  docker compose -f docker-compose.yml -f docker-compose.gpu-override.yml up -d
else
  docker compose -f docker-compose.yml up -d
fi