#!/bin/bash
# Grok Super Agent — Linux/macOS 설치 스크립트

echo ""
echo "  Grok Super Agent — Installing..."
echo ""

# 1. pip install
pip install -e .

# 2. .env 설정
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  Created .env from .env.example"
    echo "  Add your XAI_API_KEY to .env (https://console.x.ai/)"
else
    echo "  .env already exists"
fi

echo ""
echo "  Run: grok-super-agent"
echo ""
