#!/bin/bash

# Runs Django's service in order to generate a image
docker compose -f docker-compose-server.yml build

# Runs all services to achieve the expected app behavior
docker compose -f docker-compose.yml up