# Antigravity GPU Force-Acceleration Script
# ---------------------------------------------------------
# This script forces Ollama to use the NVIDIA RTX 5080 
# and ignores the integrated Intel Graphics.

Write-Host "--- Antigravity GPU Hardening ---" -ForegroundColor Cyan

# 1. Kill existing Ollama processes
Write-Host "Closing Ollama..." -ForegroundColor Yellow
Stop-Process -Name "ollama" -ErrorAction SilentlyContinue
Stop-Process -Name "Ollama" -ErrorAction SilentlyContinue

# 2. Set Environment Variables for NVIDIA Priority
Write-Host "Setting NVIDIA CUDA priority (Sovereign Mode)..." -ForegroundColor Green

# Force the specific UUID of the 5080
[System.Environment]::SetEnvironmentVariable("CUDA_VISIBLE_DEVICES", "GPU-06c60550-4dce-50ab-7cc5-4a1e298d27ab", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "127.0.0.1:11434", "User")
[System.Environment]::SetEnvironmentVariable("OLLAMA_DEBUG", "1", "User")
# Ensure it doesn't try to use the Intel chip for KV cache
[System.Environment]::SetEnvironmentVariable("OLLAMA_NUM_PARALLEL", "1", "User")

# 3. Restart Ollama
Write-Host "Restarting Ollama with NVIDIA acceleration..." -ForegroundColor Green
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama app.exe"
if (Test-Path $ollamaPath) {
    Start-Process $ollamaPath
    Write-Host "Ollama restarted. Please wait 10 seconds for it to initialize." -ForegroundColor Cyan
} else {
    Write-Host "Error: Could not find Ollama executable at $ollamaPath" -ForegroundColor Red
}

Write-Host "--- Done. Please run 'ollama ps' in 10 seconds to verify GPU offloading. ---" -ForegroundColor Cyan
