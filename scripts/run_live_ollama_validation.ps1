param([string]$BaseUrl='http://127.0.0.1:8000', [string]$Model='qwen3:4b')
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$LocalPython=Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (Test-Path $LocalPython) {
    & $LocalPython scripts\validate_local_agent.py --base-url $BaseUrl --model $Model
} else {
    & py -3.12 scripts\validate_local_agent.py --base-url $BaseUrl --model $Model
}
$ValidationCode=$LASTEXITCODE
if ($ValidationCode -eq 0) {
    Write-Host 'Actual local inference captured. Review answers before claiming quality.'
} else {
    Write-Host 'BLOCKED or PARTIAL. Start Ollama, confirm qwen3:4b, and enable local signup on the API.'
}
Write-Host 'Share only runtime\local_validation\sanitized_ollama_results.json after checking it.'
exit $ValidationCode
