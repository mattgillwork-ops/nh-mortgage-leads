#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install FastAPI, Uvicorn, and WebSocket libraries
pip install fastapi uvicorn websockets
