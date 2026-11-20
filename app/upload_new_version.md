#!/bin/bash

# Read version parts from version.json using jq
major=$(jq -r '.major' version.json)
minor=$(jq -r '.minor' version.json)
patch=$(jq -r '.patch' version.json)

# Compose version string
version="${major}.${minor}.${patch}"

echo "Building version: $version"

# Build the docker image
docker build -t ml-rest-api:latest .

# Tag images with dynamic version and latest
docker tag ml-rest-api:latest lendoo73/ml-rest-api:$version
docker tag ml-rest-api:latest lendoo73/ml-rest-api:latest

# Login (you can skip if already logged in)
docker login

# Push both tags
docker push lendoo73/ml-rest-api:$version
docker push lendoo73/ml-rest-api:latest
