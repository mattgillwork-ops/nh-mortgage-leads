#!/bin/bash

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
  echo "Creating frontend directory..."
  mkdir frontend
fi

cd frontend

# Initialize Vite + React project
npx create-vite@latest . --template react
