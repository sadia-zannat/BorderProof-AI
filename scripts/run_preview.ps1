param([switch]$SeedDemo)
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$env:APP_ENV='development'
$env:ENABLE_LOCAL_SIGNUP='1'
$env:ENABLE_DEMO_SEED='0'
$env:OLLAMA_MODEL='qwen3:4b'
if ($SeedDemo) {
    if (-not $env:DEMO_SEED_PASSWORD -or $env:DEMO_SEED_PASSWORD.Length -lt 12) {
        throw 'Set your own 12+ character DEMO_SEED_PASSWORD before using -SeedDemo.'
    }
    $env:ENABLE_DEMO_SEED='1'
}
$LocalPython=Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (Test-Path $LocalPython) {
    & $LocalPython -m uvicorn app.main:app --app-dir services\api --host 127.0.0.1 --port 8000
} else {
    & py -3.12 -m uvicorn app.main:app --app-dir services\api --host 127.0.0.1 --port 8000
}
exit $LASTEXITCODE
