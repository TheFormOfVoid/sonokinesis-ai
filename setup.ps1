<#
  Sets up this folder for an AI agent: finds the beatform tool, writes .mcp.json (used by Claude Code
  and other MCP clients that read project config), and checks the game and the Beatform loader.

  .\setup.ps1                       find beatform.exe by itself
  .\setup.ps1 -Beatform C:\path\to\beatform.exe
#>
param([string]$Beatform)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-Beatform {
    if ($env:BEATFORM_EXE -and (Test-Path $env:BEATFORM_EXE)) { return $env:BEATFORM_EXE }
    $onPath = Get-Command beatform -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Source }
    $candidates = @(
        (Join-Path $here '..\beatform\tools\cli\bin\Release\net8.0\beatform.exe'),
        (Join-Path $here '..\Beatform\tools\beatform.exe')
    )
    foreach ($dir in Get-ChildItem (Join-Path $here '..') -Directory -Filter 'Beatform*' -ErrorAction SilentlyContinue) {
        $candidates += (Join-Path $dir.FullName 'tools\beatform.exe')
    }
    foreach ($c in $candidates) { if (Test-Path $c) { return (Resolve-Path $c).Path } }
    return $null
}

if (-not $Beatform) { $Beatform = Find-Beatform }
if (-not $Beatform -or -not (Test-Path $Beatform)) {
    Write-Host "Could not find beatform.exe." -ForegroundColor Yellow
    Write-Host "Download the Beatform release and unzip it next to this folder (it has tools\beatform.exe),"
    Write-Host "or build it from the beatform repository (dotnet build -c Release tools/cli), then run:"
    Write-Host "  .\setup.ps1 -Beatform C:\path\to\beatform.exe"
    exit 1
}
$Beatform = (Resolve-Path $Beatform).Path
Write-Host "beatform: $Beatform"

$config = [ordered]@{ mcpServers = [ordered]@{ beatform = [ordered]@{ command = $Beatform; args = @('mcp') } } }
$json = $config | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText((Join-Path $here '.mcp.json'), $json, (New-Object System.Text.UTF8Encoding $false))
Write-Host "Wrote .mcp.json"

New-Item -ItemType Directory -Force (Join-Path $here 'levels') | Out-Null

Write-Host ""
Write-Host "Checking the game:"
& $Beatform game-status

Write-Host ""
Write-Host "Done. Open an AI client in this folder (for Claude Code: run 'claude' here and approve the"
Write-Host "beatform server), then start with a prompt from prompts\make-a-level.md."
Write-Host "Other clients: add this MCP server in their settings:"
Write-Host $json
