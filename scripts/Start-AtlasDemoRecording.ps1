# Start-AtlasDemoRecording.ps1
# Launches Atlas in demo recording mode with auto-scroll and opens the recording URL.

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host ""
Write-Host "=== Atlas Demo Recording Launcher ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting Streamlit..." -ForegroundColor Yellow
Start-Process "streamlit" -ArgumentList "run", "app.py" -NoNewWindow

Start-Sleep -Seconds 3

$DemoUrl = "http://localhost:8501?demo=video&autoscroll=1"
Write-Host "Opening: $DemoUrl" -ForegroundColor Green
Start-Process $DemoUrl

Write-Host ""
Write-Host "=== Recording Instructions ===" -ForegroundColor Cyan
Write-Host "  1. Start OBS or ShareX recording."
Write-Host "  2. Confirm browser is at: $DemoUrl"
Write-Host "  3. Page auto-scrolls after 3 seconds — no manual scrolling needed."
Write-Host "  4. Stop recording after the footer disclaimer (~75-80 seconds)."
Write-Host ""
Write-Host "OBS Browser Source URL:  $DemoUrl" -ForegroundColor Yellow
Write-Host "  -> Add Browser Source, paste URL, set 1920x1080, click Refresh."
Write-Host "  -> Start recording, then click Refresh in OBS — scroll starts in 3s."
Write-Host ""
Write-Host "Manual scroll mode (no autoscroll): http://localhost:8501?demo=video" -ForegroundColor DarkGray
Write-Host "Normal app:                          http://localhost:8501" -ForegroundColor DarkGray
Write-Host ""
