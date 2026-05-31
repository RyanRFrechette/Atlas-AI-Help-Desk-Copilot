# Start-AtlasDemoRecording.ps1
# Launches Atlas in demo recording mode and opens the recording URL.

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host ""
Write-Host "=== Atlas Demo Recording Launcher ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Streamlit..." -ForegroundColor Yellow
Start-Process "streamlit" -ArgumentList "run", "app.py" -NoNewWindow

Start-Sleep -Seconds 3

$DemoUrl = "http://localhost:8501?demo=video"
Write-Host "Opening: $DemoUrl" -ForegroundColor Green
Start-Process $DemoUrl

Write-Host ""
Write-Host "=== Recording Instructions ===" -ForegroundColor Cyan
Write-Host "  1. Start OBS or ShareX recording."
Write-Host "  2. Confirm browser is at: $DemoUrl"
Write-Host "  3. Scroll slowly top to bottom over 60-90 seconds."
Write-Host "  4. Pause 2-3 seconds on triage cards and escalation banner."
Write-Host "  5. Stop recording after the footer disclaimer."
Write-Host ""
Write-Host "Normal app (no demo mode): http://localhost:8501" -ForegroundColor DarkGray
Write-Host ""
