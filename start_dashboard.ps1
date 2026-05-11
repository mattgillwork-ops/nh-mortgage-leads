# Launch the Anti-Gravity Command Center via Docker
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Launching Anti-Gravity Command Center   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$WorkspacePath = (Get-Item .).FullName

Write-Host "Starting secure sandbox container on port 8000..." -ForegroundColor Yellow

# Run the container in detached mode, map port 8000, mount workspace
docker run -d --name antigravity-dashboard -p 8000:8000 -v "${WorkspacePath}:/workspace" -w /workspace anti-sandbox python backend/app.py

Write-Host "Command Center is running!" -ForegroundColor Green
Write-Host "Open your browser to: http://localhost:8000" -ForegroundColor Cyan
Write-Host "To stop the dashboard, run: docker stop antigravity-dashboard; docker rm antigravity-dashboard" -ForegroundColor Gray
