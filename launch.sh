#!/bin/bash
# Phase 4: Launch Command Center
echo "Starting Backend..."
python3 backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!

echo "Starting Frontend..."
cd frontend && npm install && npm run dev -- --host > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "Waiting for servers to warm up..."
sleep 10

echo "Creating Public Tunnel..."
npx localtunnel --port 5173 > lt.log 2>&1 &
LT_PID=$!

sleep 5
URL=$(grep -o "https://[a-zA-Z0-9.-]*\.loca\.lt" lt.log)
echo "------------------------------------------------"
echo "COMMAND CENTER ONLINE"
echo "Public URL: $URL"
echo "Local URL: http://localhost:5173"
echo "------------------------------------------------"

# Keep alive
wait $LT_PID
