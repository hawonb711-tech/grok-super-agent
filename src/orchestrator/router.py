"""AI 라우터 - 태스크 유형에 따라 Grok/Claude/GPT 선택. 디폴트는 Grok."""

import re
from enum import Enum


class ModelId(str, Enum):
    """지원 모델 ID."""

    GROK = "grok"
    CLAUDE = "claude"
    OPENAI = "openai"


# 라우팅 키워드 (태스크 유형 → 모델)
ROUTING_RULES = [
    # 실시간/X → Grok
    (r"(지금|오늘|최근|트렌드|실시간|x\.ai|엘론|트윗)", ModelId.GROK),
    # 코드/문서 → Claude
    (r"(코드|리팩터|문서화|리팩토링|refactor|document)", ModelId.CLAUDE),
    # 수학/알고리즘 → Grok
    (r"(수학|알고리즘|계산|algorithm|math)", ModelId.GROK),
    # 비전/이미지 → OpenAI (멀티모달)
    (r"(이미지|화면|스크린샷|image|screenshot)", ModelId.OPENAI),
    # 일반 → GPT
    (r"(요약|정리|설명|summary|explain)", ModelId.OPENAI),
]


class Router:
    """태스크에 맞는 AI 선택. 매칭 없으면 Grok (디폴트)."""

    def __init__(self) -> None:
        self._rules = [(re.compile(p, re.I), m) for p, m in ROUTING_RULES]

    def route(self, task: str, context: str = "") -> ModelId:
        """태스크 + 컨텍스트에 따라 모델 선택."""
        text = f"{task} {context}".lower()
        for pattern, model in self._rules:
            if pattern.search(text):
                return model
        return ModelId.GROK  # 디폴트: Grok
