# Installs every agent from Dev Instincts into ~/.claude/agents and checks the whole setup.
# Run after any change to agent/*.md, and before each round:
#   powershell -ExecutionPolicy Bypass -File "$env:DEV_INSTINCTS_HOME\agent\sync-agents.ps1"
# -CheckOnly reports without copying.
param([switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
$repo = $env:DEV_INSTINCTS_HOME
if (-not $repo) { Write-Output "DEV_INSTINCTS_HOME is not set (user environment variable)."; exit 1 }
if (-not (Test-Path (Join-Path $repo 'DEV-INSTINCTS.md'))) { Write-Output "$repo is not a Dev Instincts repo."; exit 1 }
$dest = Join-Path $env:USERPROFILE '.claude\agents'
New-Item -ItemType Directory -Force $dest | Out-Null
$bad = 0

foreach ($a in 'instinct-reviewer', 'dev-architect', 'senior-coder') {
    $src = Join-Path $repo "agent\$a.md"
    $dst = Join-Path $dest "$a.md"
    if (-not $CheckOnly) { Copy-Item $src $dst -Force }
    if ((Test-Path $dst) -and ((Get-FileHash $src).Hash -eq (Get-FileHash $dst).Hash)) {
        Write-Output "OK         $a"
    } else {
        Write-Output "DIFFERENT  $a"; $bad++
    }
}

# Memory that names a Dev Instincts folder other than DEV_INSTINCTS_HOME.
$roots = @('projects', 'agent-memory') | ForEach-Object { Join-Path $env:USERPROFILE ".claude\$_" } | Where-Object { Test-Path $_ }
$here = $repo.TrimEnd('\')
foreach ($m in (Get-ChildItem $roots -Recurse -File -Filter *.md -ErrorAction SilentlyContinue |
        Select-String -Pattern '[A-Za-z]:\\[^\s`"'')]*\\dev-instincts(?![-\w])' -AllMatches)) {
    foreach ($v in $m.Matches.Value) {
        if ($v -ne $here) { Write-Output "STALE PATH $($m.Path):$($m.LineNumber)  $v"; $bad++ }
    }
}

if ($bad) { Write-Output "$bad problem(s). Fix them, then restart Claude Code."; exit 1 }
Write-Output "In sync: all agents match Dev Instincts and no memory names another location. Restart Claude Code if it was open."
