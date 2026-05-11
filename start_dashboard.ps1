# Launch the Anti-Gravity Command Center via Docker
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Launching Anti-Gravity Command Center   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$WorkspacePath = (Get-Item .).FullName

Write-Host "Starting secure agency infrastructure via Docker Compose..." -ForegroundColor Yellow

# Start the services
docker-compose up -d

Write-Host "Command Center and Iron Sentry are running!" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Iron Sentry: listening on port 2525" -ForegroundColor Cyan
Write-Host "To stop the agency, run: docker-compose down" -ForegroundColor Gray
