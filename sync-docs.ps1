<#
  Copies Beatform's guides into docs/ (for agents that read files instead of using the docs tool).
  .\sync-docs.ps1 [-Beatform ..\beatform]     the Beatform repository or release folder
#>
param([string]$Beatform = (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '..\beatform'))

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$src = Join-Path $Beatform 'docs'
if (-not (Test-Path (Join-Path $src 'scripting.md'))) { throw "no docs in $src" }
$dest = Join-Path $here 'docs'
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item (Join-Path $src '*.md') $dest -Force
# The format lives in spec/ in the repository and in docs/ in the release.
$spec = Join-Path $Beatform 'spec\level-format.md'
if (Test-Path $spec) { Copy-Item $spec (Join-Path $dest 'level-format.md') -Force }
foreach ($f in Get-ChildItem $dest -Filter *.md) {
    $text = [System.IO.File]::ReadAllText($f.FullName)
    $text = $text.Replace('../spec/level-format.md', 'level-format.md')
    [System.IO.File]::WriteAllText($f.FullName, $text, (New-Object System.Text.UTF8Encoding $false))
}
Write-Host "Copied the docs from $src"
