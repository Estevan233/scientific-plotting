<#
.SYNOPSIS
    One-click installer for scientific-plotting skill on Windows.
.DESCRIPTION
    Installs the scientific-plotting skill to Antigravity / Gemini CLI global or workspace directory.
.PARAMETER Scope
    'Global' (default, installs to $HOME\.gemini\skills\scientific-plotting)
    'Workspace' (installs to .agents\skills\scientific-plotting in current directory)
.PARAMETER Pip
    If specified, installs scientific-plotting as an editable Python package via pip.
.EXAMPLE
    .\install.ps1
    .\install.ps1 -Scope Workspace
    .\install.ps1 -Pip
#>

[CmdletBinding()]
param (
    [ValidateSet("Global", "Workspace")]
    [string]$Scope = "Global",

    [switch]$Pip
)

$ErrorActionPreference = "Stop"

$RepoRoot = $PSScriptRoot

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "   Scientific-Plotting Skill Installer (Windows)       " -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

if ($Scope -eq "Global") {
    $TargetDir = Join-Path $HOME ".gemini\skills\scientific-plotting"
} else {
    $TargetDir = Join-Path (Get-Location) ".agents\skills\scientific-plotting"
}

Write-Host "[*] Target Installation Scope : $Scope" -ForegroundColor Yellow
Write-Host "[*] Destination Path          : $TargetDir" -ForegroundColor Yellow

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$ItemsToCopy = @(
    "SKILL.md",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "LICENSE",
    ".cursor",
    "scripts",
    "scientific_plotting",
    "examples",
    "references"
)

foreach ($item in $ItemsToCopy) {
    $sourcePath = Join-Path $RepoRoot $item
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $TargetDir -Recurse -Force
        Write-Host "  [+] Copied: $item" -ForegroundColor Green
    }
}

if ($Pip) {
    Write-Host "[*] Installing Python package via pip (editable mode)..." -ForegroundColor Yellow
    try {
        pip install -e $TargetDir
        Write-Host "  [+] Pip install completed successfully." -ForegroundColor Green
    } catch {
        Write-Warning "Pip install failed. You can run 'pip install -e $TargetDir' manually."
    }
}

Write-Host "`n[OK] Installation completed successfully!" -ForegroundColor Green
Write-Host "Skill is now active and ready for Antigravity, Gemini CLI, Cursor, and Claude Code." -ForegroundColor Cyan

