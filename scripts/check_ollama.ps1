# V5.1: no paid credentials required. Run AFTER installing Ollama on Windows.
$ErrorActionPreference = 'Stop'
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host 'Ollama not found. Install from https://ollama.com/download/windows and REOPEN PowerShell.' -ForegroundColor Yellow
    exit 1
}
Write-Host 'Installed Ollama:'
ollama --version
Write-Host 'Locally downloaded models:'
ollama list
try {
    $tags=Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 6
    if (-not ($tags.models | Where-Object { $_.name -eq 'qwen3:4b' -or $_.model -eq 'qwen3:4b' })) {
        Write-Host 'qwen3:4b is missing. Run: ollama pull qwen3:4b' -ForegroundColor Yellow
        exit 2
    }
    Write-Host 'Ollama API is reachable, qwen3:4b downloaded.' -ForegroundColor Green
} catch {
    Write-Host 'Ollama API is not reachable. Launch the Ollama Windows application, then retry.' -ForegroundColor Yellow
    exit 3
}
