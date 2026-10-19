<#
  Sets up this folder for an AI agent: finds the sonokinesis tool, writes .mcp.json (used by Claude Code
  and other MCP clients that read project config), and checks the game and the Sonokinesis loader.

  .\setup.ps1                       find sonokinesis.exe by itself
  .\setup.ps1 -Sonokinesis C:\path\to\sonokinesis.exe
#>
param([string]$Sonokinesis)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-Sonokinesis {
    if ($env:SONOKINESIS_EXE -and (Test-Path $env:SONOKINESIS_EXE)) { return $env:SONOKINESIS_EXE }
    $onPath = Get-Command sonokinesis -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Source }
    $candidates = @(
        # Downloaded from the Sonokinesis app (its Create tab).
        (Join-Path $env:LOCALAPPDATA 'Programs\Sonokinesis\tools\sonokinesis.exe'),
        (Join-Path $here '..\sonokinesis\tools\cli\bin\Release\net8.0\sonokinesis.exe'),
        (Join-Path $here '..\Sonokinesis\tools\sonokinesis.exe')
    )
    foreach ($dir in Get-ChildItem (Join-Path $here '..') -Directory -Filter 'Sonokinesis*' -ErrorAction SilentlyContinue) {
        $candidates += (Join-Path $dir.FullName 'tools\sonokinesis.exe')
    }
    foreach ($c in $candidates) { if (Test-Path $c) { return (Resolve-Path $c).Path } }
    return $null
}

if (-not $Sonokinesis) { $Sonokinesis = Find-Sonokinesis }
if (-not $Sonokinesis -or -not (Test-Path $Sonokinesis)) {
    Write-Host "Could not find sonokinesis.exe." -ForegroundColor Yellow
    Write-Host "Install the Sonokinesis app and press 'Download the AI tool' on its Create tab (or unzip"
    Write-Host "Sonokinesis-AI-Tool from the releases next to this folder),"
    Write-Host "or build it from the sonokinesis repository (dotnet build -c Release tools/cli), then run:"
    Write-Host "  .\setup.ps1 -Sonokinesis C:\path\to\sonokinesis.exe"
    exit 1
}
$Sonokinesis = (Resolve-Path $Sonokinesis).Path
Write-Host "sonokinesis: $Sonokinesis"

$config = [ordered]@{ mcpServers = [ordered]@{ sonokinesis = [ordered]@{ command = $Sonokinesis; args = @('mcp') } } }
$json = $config | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText((Join-Path $here '.mcp.json'), $json, (New-Object System.Text.UTF8Encoding $false))
Write-Host "Wrote .mcp.json"

New-Item -ItemType Directory -Force (Join-Path $here 'levels') | Out-Null

Write-Host ""
Write-Host "Checking the game:"
& $Sonokinesis game-status

Write-Host ""
Write-Host "Done. Open an AI client in this folder (for Claude Code: run 'claude' here and approve the"
Write-Host "sonokinesis server), then start with a prompt from prompts\make-a-level.md."
Write-Host "Other clients: add this MCP server in their settings:"
Write-Host $json
