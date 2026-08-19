# health-check.ps1 - read-only machine health snapshot (PowerShell 5.1 safe)
# Usage: powershell -ExecutionPolicy Bypass -File "C:\Users\subha\.claude\skills\machine-debugging-playbook\scripts\health-check.ps1"
# Writes nothing; changes nothing; installs nothing.

$ErrorActionPreference = 'Continue'
Write-Output ("=== MACHINE HEALTH CHECK  {0} ===" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))

Write-Output ""
Write-Output "--- Tool versions (expected as of 2026-07-06: git 2.49 / py 3.13.5 / uv 0.11 / node 22 / go 1.24 / cargo 1.94 / java 21 / docker 28 / ollama 0.17) ---"
$tools = @(
    @{ n = 'git';      a = '--version' },
    @{ n = 'python';   a = '--version' },
    @{ n = 'uv';       a = '--version' },
    @{ n = 'node';     a = '--version' },
    @{ n = 'npm';      a = '--version' },
    @{ n = 'go';       a = 'version' },
    @{ n = 'cargo';    a = '--version' },
    @{ n = 'java';     a = '-version' },
    @{ n = 'docker';   a = '--version' },
    @{ n = 'ollama';   a = '--version' },
    @{ n = 'claude';   a = '--version' },
    @{ n = 'tectonic'; a = '--version' }
)
foreach ($t in $tools) {
    $cmd = Get-Command $t.n -ErrorAction SilentlyContinue
    if ($cmd) {
        # cmd-level redirect avoids PS 5.1 NativeCommandError wrapping (java prints version to stderr)
        $v = cmd /c ("{0} {1} 2>&1" -f $t.n, $t.a) | Select-Object -First 1
        Write-Output ("{0,-10} {1}" -f $t.n, $v)
    } else {
        Write-Output ("{0,-10} NOT ON PATH" -f $t.n)
    }
}

Write-Output ""
Write-Output "--- Python interpreter inventory (multi-python is THE classic trap here) ---"
$sysPy = Get-Command python -ErrorAction SilentlyContinue
if ($sysPy) { Write-Output ("PATH python : {0}" -f $sysPy.Source) } else { Write-Output "PATH python : NONE" }
if (Test-Path "$env:USERPROFILE\venv\pyvenv.cfg") { Write-Output ("home venv   : {0}\venv" -f $env:USERPROFILE) }
$repoRoot = "$env:USERPROFILE\Projects"
if (Test-Path $repoRoot) {
    foreach ($d in (Get-ChildItem $repoRoot -Directory -ErrorAction SilentlyContinue)) {
        foreach ($v in @('venv', '.venv')) {
            if (Test-Path (Join-Path $d.FullName "$v\pyvenv.cfg")) {
                Write-Output ("repo venv   : {0}\{1}" -f $d.Name, $v)
            }
        }
    }
}
if ($env:VIRTUAL_ENV) { Write-Output ("ACTIVE venv : {0}  <-- affects which packages import!" -f $env:VIRTUAL_ENV) }

Write-Output ""
Write-Output "--- graphifyy engine vs deployed skill version (must match) ---"
$pipVer = cmd /c "python -m pip show graphifyy 2>&1" | Select-String '^Version' | ForEach-Object { ($_ -split ':\s*')[1] }
$skillVerFile = "$env:USERPROFILE\.claude\skills\graphify\.graphify_version"
$skillVer = if (Test-Path $skillVerFile) { (Get-Content $skillVerFile -Raw).Trim() } else { 'MISSING' }
Write-Output ("pip graphifyy : {0}" -f $(if ($pipVer) { $pipVer } else { 'NOT INSTALLED in PATH python' }))
Write-Output ("skill version : {0}" -f $skillVer)
if ($pipVer -and $skillVer -ne 'MISSING' -and $pipVer -ne $skillVer) {
    Write-Output "  !! DRIFT: user should run: graphify install --platform windows"
}

Write-Output ""
Write-Output "--- PATH audit ---"
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
Write-Output ("~\bin on User PATH : {0}" -f ($userPath -like "*$env:USERPROFILE\bin*"))

Write-Output ""
Write-Output "--- Claude config safety (runtimeads incident guard - see machine-failure-archaeology) ---"
Write-Output ("~\.runtimeads exists : {0}  (True would mean the ad-hook is BACK)" -f (Test-Path "$env:USERPROFILE\.runtimeads"))
try {
    $settings = Get-Content "$env:USERPROFILE\.claude\settings.json" -Raw | ConvertFrom-Json
    $hookProps = @()
    if ($settings.hooks) { $hookProps = @($settings.hooks.PSObject.Properties) }
    Write-Output ("settings.json hook events configured : {0}  (expected 0 as of 2026-07-06)" -f $hookProps.Count)
    if ($hookProps.Count -gt 0) {
        foreach ($p in $hookProps) { Write-Output ("  hook event: {0}" -f $p.Name) }
        Write-Output "  ^ verify with the user that these are intentional"
    }
} catch { Write-Output "settings.json unreadable - investigate" }

Write-Output ""
Write-Output "--- Dirty-repo report (uncommitted WIP is NORMAL here - do not clean up) ---"
if (Test-Path $repoRoot) {
    foreach ($d in (Get-ChildItem $repoRoot -Directory -ErrorAction SilentlyContinue)) {
        if (Test-Path (Join-Path $d.FullName '.git')) {
            $n = (git -C $d.FullName status --porcelain 2>$null | Measure-Object).Count
            if ($n -gt 0) { Write-Output ("{0,-32} dirty={1}" -f $d.Name, $n) }
        }
    }
}

Write-Output ""
Write-Output "--- Disk ---"
$c = Get-PSDrive C
Write-Output ("C: free {0:N1} GB / used {1:N1} GB" -f ($c.Free / 1GB), ($c.Used / 1GB))

Write-Output ""
Write-Output "=== END HEALTH CHECK ==="
