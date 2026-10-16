<#
.SYNOPSIS
    One-click setup and launcher for IG Growth Prompts on Windows.

.DESCRIPTION
    Checks Python 3.10+ runtime, installs the igprompts package locally in editable mode,
    verifies quality gates, and optionally launches the desktop GUI.

.PARAMETER LaunchGUI
    Launch the desktop workbench immediately after setup. Default: $true.
#>
[CmdletBinding()]
param(
    [switch]$LaunchGUI = $true,
    [switch]$RunDevCheck = $false
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   IG Growth Prompts - Windows Setup & Environment" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python installation
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    Write-Error "Python not found! Please install Python 3.10 or higher from https://python.org or via 'winget install Python.Python.3.13'"
    exit 1
}

$PyVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "==> Detected Python $PyVersion" -ForegroundColor Green

# 2. Install package in editable mode
$RepoRoot = $PSScriptRoot
Set-Location $RepoRoot

Write-Host "==> Installing igprompts package locally (pip install -e .)..." -ForegroundColor Cyan
python -m pip install --quiet -e .

# 3. Optional quality gate run
if ($RunDevCheck) {
    Write-Host "==> Running local verification gates..." -ForegroundColor Cyan
    & ./tools/dev_check.ps1
}

Write-Host "==> Setup completed successfully!" -ForegroundColor Green
Write-Host "    You can now run 'igprompts --help' or 'igprompts gui' anywhere in terminal." -ForegroundColor DarkGray

# 4. Optional Launch GUI
if ($LaunchGUI) {
    Write-Host "==> Launching Desktop GUI Workbench..." -ForegroundColor Cyan
    python -m igprompts gui
}
