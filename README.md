# Grok Super Agent

**멀티 AI 오케스트레이션 + Computer Use** — 제때 제때 AI를 불러와 업무 효율 1000%.

x.ai · Tesla · SpaceX — Truth-seeking AI

---

## 빠른 설치

```bash
# 1. 클론 또는 다운로드 후
cd "let's open"

# 2. 설치 (한 줄)
pip install -e .

# Windows: install.ps1 실행
# Linux/macOS: ./install.sh 실행

# 3. .env 설정
cp .env.example .env
# .env에 XAI_API_KEY=your_key 입력 (https://console.x.ai/)

# 4. 실행
grok-super-agent
# 또는: python -m src.cli

# Windows 한글 깨짐 시: chcp 65001 후 실행
```

---

## 실행

```bash
grok-super-agent
```

- **[1] ReAct** — 웹 검색, 코드 실행, 파일 읽기/쓰기
- **[2] Computer Use** — 화면 제어 + 멀티 AI (Grok/Claude/GPT)

---

## Features

- **Grok Super Agent**: 디폴트 Grok, 멀티 AI 라우팅
- **Computer Use**: CUP 기반 화면 제어
- **멀티 AI**: 태스크 유형별 Grok/Claude/GPT 자동 선택

---

## API

```bash
uvicorn src.api.server:app --reload
# POST /task  POST /computer-use
```

---

## License

MIT
