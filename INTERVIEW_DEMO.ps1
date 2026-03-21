#!/usr/bin/env powershell
<#
INTERVIEW DEMO SCRIPT
Copy and paste these commands one-by-one to show your network automation project
#>

# ============================================================
# DEMO SETUP - Do this BEFORE your interview
# ============================================================

Write-Host "
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NETWORK AUTOMATION PROJECT DEMO                           ║
║                      Real Docker Container Automation                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# Step 1: Navigate to your project
Write-Host "[STEP 1] Navigating to project directory..." -ForegroundColor Green
cd "E:\networking project\python_networking"
pwd
Write-Host ""

# ============================================================
# DEMO PART 1: Show Project Structure
# ============================================================

Write-Host "[STEP 2] Showing project structure..." -ForegroundColor Green
Get-ChildItem -Path "." | Select-Object Name, @{Name='Type'; Expression={if($_.PSIsContainer) {'Folder'} else {'File'}}}
Write-Host ""

# ============================================================
# DEMO PART 2: Start Docker Containers
# ============================================================

Write-Host "[STEP 3] Starting Docker containers..." -ForegroundColor Green
Write-Host "Command: docker-compose up -d" -ForegroundColor Yellow
docker-compose up -d
Write-Host ""

Write-Host "[STEP 4] Waiting for containers to initialize (20 seconds)..." -ForegroundColor Green
Start-Sleep -Seconds 20
Write-Host ""

# ============================================================
# DEMO PART 3: Verify Containers Running
# ============================================================

Write-Host "[STEP 5] Verifying containers are running..." -ForegroundColor Green
Write-Host "Command: docker ps" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

# ============================================================
# DEMO PART 4: Show Current Device State (BEFORE)
# ============================================================

Write-Host "[STEP 6] Current device state (BEFORE automation):" -ForegroundColor Green
Write-Host "Command: docker exec router1 hostname" -ForegroundColor Yellow
docker exec router1 hostname
Write-Host ""

Write-Host "Command: docker exec router1 ls /etc/config-* 2>/dev/null || echo 'No config file yet'" -ForegroundColor Yellow
docker exec router1 sh -c "ls /etc/config-* 2>/dev/null || echo 'No config file yet'"
Write-Host ""

# ============================================================
# DEMO PART 5: Show Automation Script
# ============================================================

Write-Host "[STEP 7] Our automation script:" -ForegroundColor Green
Write-Host "Location: ./network-automation/deploy_simple.py" -ForegroundColor Yellow
Write-Host "Contents highlighted below:" -ForegroundColor Yellow
Write-Host "-" * 60
Get-Content "./network-automation/deploy_simple.py" | Select-Object -First 20
Write-Host "    ... (more code)" -ForegroundColor Gray
Write-Host "-" * 60
Write-Host ""

# ============================================================
# DEMO PART 6: Show Device Inventory
# ============================================================

Write-Host "[STEP 8] Device inventory (devices.json):" -ForegroundColor Green
Write-Host "Command: Get-Content ./network-automation/devices.json" -ForegroundColor Yellow
Get-Content "./network-automation/devices.json" | Format-List
Write-Host ""

# ============================================================
# DEMO PART 7: Run Automation
# ============================================================

Write-Host "[STEP 9] Running network automation deployment..." -ForegroundColor Green
Write-Host "Command: python ./network-automation/deploy_simple.py" -ForegroundColor Yellow
Write-Host "-" * 60
cd "./network-automation"
python deploy_simple.py
Write-Host "-" * 60
Write-Host ""

# ============================================================
# DEMO PART 8: Verify Changes (AFTER)
# ============================================================

Write-Host "[STEP 10] Device state AFTER automation:" -ForegroundColor Green
Write-Host "Command: docker exec router1 cat /etc/config-router1.txt" -ForegroundColor Yellow
docker exec router1 cat /etc/config-router1.txt
Write-Host ""

Write-Host "Command: docker exec router2 cat /etc/config-router2.txt" -ForegroundColor Yellow
docker exec router2 cat /etc/config-router2.txt
Write-Host ""

# ============================================================
# DEMO PART 9: Show Deployment Log
# ============================================================

Write-Host "[STEP 11] Deployment log:" -ForegroundColor Green
Write-Host "Location: ./logs/" -ForegroundColor Yellow
Get-ChildItem "./logs/" | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object {
    Write-Host "Latest log: $($_.Name)" -ForegroundColor Yellow
    Write-Host "-" * 60
    Get-Content $_.FullName | Select-Object -Last 30
    Write-Host "-" * 60
}
Write-Host ""

# ============================================================
# DEMO COMPLETE
# ============================================================

Write-Host "
╔══════════════════════════════════════════════════════════════════════════════╗
║                           DEMO COMPLETE                                      ║
║                                                                              ║
║  Key Talking Points:                                                         ║
║  1. This connects to REAL Docker containers (not mocked)                    ║
║  2. The automation creates configuration files via docker exec              ║
║  3. Before/after shows the proof it actually deployed                       ║
║  4. This scales from 2 containers to 1000+ real switches                    ║
║  5. Same Python code works with SSH to real Arista hardware                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

Write-Host "Interview Ready! You can now explain how this demonstrates:" -ForegroundColor Green
Write-Host "  • Real network automation (not simulated)" -ForegroundColor White
Write-Host "  • Infrastructure-as-Code principles" -ForegroundColor White
Write-Host "  • Python best practices (logging, error handling)" -ForegroundColor White
Write-Host "  • Scalability (2 devices NOW, 1000s possible)" -ForegroundColor White
Write-Host "  • Production-grade deployment workflows" -ForegroundColor White
