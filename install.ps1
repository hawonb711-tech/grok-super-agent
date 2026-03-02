# Grok Super Agent — Windows 설치 스크립트
Write-Host "`n  Grok Super Agent — Installing...`n" -ForegroundColor Cyan

# 1. pip install
pip install -e "."

# 2. .env 설정
$envExample = ".env.example"
$envFile = ".env"
if (-not (Test-Path $envFile)) {
    Copy-Item $envExample $envFile
    Write-Host "  Created .env from .env.example" -ForegroundColor Green
    Write-Host "  Add your XAI_API_KEY to .env (https://console.x.ai/)`n" -ForegroundColor Yellow
} else {
    Write-Host "  .env already exists`n" -ForegroundColor Green
}

Write-Host "  Run: grok-super-agent`n" -ForegroundColor Cyan
