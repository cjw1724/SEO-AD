# Blogin 365 AI Holdings - Windows Task Scheduler Auto-Registration Script
$TaskName = "Blogin365AI_AutonomousCompany"
$ProjectDir = "d:\SEO AD"
$PythonExe = "d:\SEO AD\venv\Scripts\python.exe"
$ScriptPath = "d:\SEO AD\engine\company_runtime.py"
$Arguments = "`"$ScriptPath`" --once"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " [Blogin 365 AI Holdings] Windows Task Scheduler Registration" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Verification of environment files
if (-not (Test-Path $PythonExe)) {
    Write-Error "Python virtual environment not found: $PythonExe"
    exit 1
}

if (-not (Test-Path $ScriptPath)) {
    Write-Error "Runtime script not found: $ScriptPath"
    exit 1
}

Write-Host "[1/3] Checking and cleaning existing task..." -ForegroundColor Yellow
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Write-Host " -> Existing task [$TaskName] found. Re-registering..." -ForegroundColor Gray
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Write-Host "[2/3] Building scheduled action and 3 daily triggers (09:00, 15:00, 21:00)..." -ForegroundColor Yellow
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $Arguments -WorkingDirectory $ProjectDir

$TriggerMorning   = New-ScheduledTaskTrigger -Daily -At 09:00
$TriggerAfternoon = New-ScheduledTaskTrigger -Daily -At 15:00
$TriggerNight     = New-ScheduledTaskTrigger -Daily -At 21:00
$Triggers = @($TriggerMorning, $TriggerAfternoon, $TriggerNight)

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -WakeToRun `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 5) `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Write-Host "[3/3] Registering task in Windows Task Scheduler..." -ForegroundColor Yellow
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Triggers `
        -Settings $Settings `
        -Description "Blogin 365 AI Holdings 24/7 Autonomous Media Engine v6.0" | Out-Null

    Write-Host "`n=================================================================" -ForegroundColor Green
    Write-Host " Task Scheduler Registration SUCCESS! [$TaskName]" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
    Write-Host " Program  : $PythonExe"
    Write-Host " Arguments: $Arguments"
    Write-Host " Cwd      : $ProjectDir"
    Write-Host " Triggers : Daily at 09:00, 15:00, 21:00 (365 Days Autonomous)"
    Write-Host " Check    : Get-ScheduledTask -TaskName '$TaskName'"
    Write-Host "=================================================================`n" -ForegroundColor Green
} catch {
    Write-Host "PowerShell cmdlets encountered an issue ($($_)), falling back to schtasks.exe..." -ForegroundColor Yellow
    $schArg = "`"$PythonExe`" `"$ScriptPath`" --once"
    & schtasks.exe /Create /F /TN $TaskName /TR $schArg /SC DAILY /ST 09:00 /RI 360 /DU 24:00
    Write-Host "schtasks.exe fallback registration completed!" -ForegroundColor Green
}
