<#
.SYNOPSIS
    Builds portable standalone executable and optional Windows installer using SemVer naming.

.DESCRIPTION
    Extracts semantic version from igprompts/__init__.py, compiles portable single-file binary
    (igprompts-gui-vX.Y.Z-portable.exe) via PyInstaller, and compiles Windows installer
    (igprompts-setup-vX.Y.Z.exe) via Inno Setup (ISCC) if available.
#>
[CmdletBinding()]
param(
    [string]$OutputDir = "dist"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

# 1. Resolve Semantic Version from igprompts/__init__.py
$InitContent = Get-Content -Path "igprompts/__init__.py" -Raw
if ($InitContent -match '__version__\s*=\s*["'']([^"'']+)["'']') {
    $SemVer = $Matches[1]
} else {
    $SemVer = "0.5.0"
}
Write-Host "==> Target Semantic Version: v$SemVer" -ForegroundColor Cyan

# 2. Check PyInstaller
$PyInstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $PyInstaller) {
    Write-Warning "PyInstaller not found in PATH."
    Write-Host "Please install it with: pip install pyinstaller" -ForegroundColor Yellow
    exit 1
}

# Clean previous build artifacts
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path $OutputDir) { Remove-Item -Recurse -Force $OutputDir }
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# 3. Build Portable Executable
Write-Host "==> Compiling standalone portable binary with PyInstaller..." -ForegroundColor Cyan

$EntryScript = "launcher.py"
@'
from igprompts.gui import launch_gui
if __name__ == "__main__":
    launch_gui()
'@ | Set-Content -Path $EntryScript -Encoding utf8

try {
    pyinstaller `
        --noconfirm `
        --onefile `
        --windowed `
        --name "igprompts-gui" `
        --add-data "prompts;prompts" `
        --add-data "examples;examples" `
        --hidden-import "igprompts" `
        --hidden-import "tkinter" `
        --distpath $OutputDir `
        $EntryScript
}
finally {
    if (Test-Path $EntryScript) {
        Remove-Item -Force $EntryScript
    }
}

$DefaultExe = Join-Path $OutputDir "igprompts-gui.exe"
$PortableExe = Join-Path $OutputDir "igprompts-gui-v${SemVer}-portable.exe"

if (Test-Path $DefaultExe) {
    Copy-Item -Path $DefaultExe -Destination $PortableExe -Force
    $SizeMB = [math]::Round((Get-Item $PortableExe).Length / 1MB, 2)
    Write-Host "==> Portable standalone build successful: $PortableExe ($SizeMB MB)" -ForegroundColor Green
} else {
    Write-Error "PyInstaller build failed: $DefaultExe not found."
    exit 1
}

# 4. Check Inno Setup (ISCC) for Windows Setup Installer
Write-Host "==> Checking Inno Setup Compiler (ISCC)..." -ForegroundColor Cyan
$ISCC = Get-Command iscc -ErrorAction SilentlyContinue

if (-not $ISCC) {
    # Check common Inno Setup paths on Windows
    $CommonPaths = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
        "${env:LOCALAPPDATA}\Programs\Inno Setup 6\ISCC.exe"
    )
    foreach ($p in $CommonPaths) {
        if (Test-Path $p) {
            $ISCC = $p
            break
        }
    }
}

if ($ISCC) {
    Write-Host "==> Compiling Windows Setup Installer with Inno Setup..." -ForegroundColor Cyan
    & $ISCC "tools/installer.iss" "/DMyAppVersion=$SemVer"
    $InstallerExe = Join-Path $OutputDir "igprompts-setup-v${SemVer}.exe"
    if (Test-Path $InstallerExe) {
        $InstSizeMB = [math]::Round((Get-Item $InstallerExe).Length / 1MB, 2)
        Write-Host "==> Setup Installer built successfully: $InstallerExe ($InstSizeMB MB)" -ForegroundColor Green
    }
} else {
    Write-Host "==> Note: Inno Setup (ISCC) not found. Skipped installer (.exe) generation." -ForegroundColor Yellow
    Write-Host "    To build setup installer, install Inno Setup: winget install JRSoftware.InnoSetup" -ForegroundColor DarkGray
}

Write-Host "==> Packaging complete! Artifacts in $OutputDir/" -ForegroundColor Green
