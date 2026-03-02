"""CUP (Computer Use Protocol) client wrapper."""

from typing import Any

try:
    import cup
    from cup import Session
except ImportError:
    cup = None
    Session = None


class CUPClient:
    """CUP 기반 화면 제어 클라이언트."""

    def __init__(self) -> None:
        if cup is None or Session is None:
            raise ImportError(
                "computeruseprotocol not installed. Run: pip install computeruseprotocol[mcp]"
            )
        self._session = Session()

    def snapshot(self, scope: str = "foreground") -> str:
        """화면/앱 UI 트리 캡처 (LLM 컨텍스트용 compact 텍스트)."""
        return self._session.snapshot(
            scope=scope,
            compact=True,
        )

    def snapshot_raw(self, scope: str = "foreground") -> dict:
        """화면을 CUP envelope dict로 캡처."""
        return self._session.snapshot(
            scope=scope,
            compact=False,
        )

    def overview(self) -> str:
        """열린 창 목록만 (가벼움)."""
        return self._session.snapshot(scope="overview", compact=True)

    def action(self, element_id: str, action: str, **params: Any) -> dict:
        """요소에 액션 실행 (click, type 등).

        Args:
            element_id: 트리에서의 요소 ID (e.g. "e14")
            action: CUP 액션 (click, type, toggle 등)
            **params: 액션 파라미터 (value for type 등)

        Returns:
            ActionResult를 dict로 (success, message, error)
        """
        result = self._session.action(element_id, action, **params)
        return {
            "success": result.success,
            "message": getattr(result, "message", ""),
            "error": getattr(result, "error", None),
        }

    def press(self, keys: str) -> dict:
        """키보드 단축키 전송 (e.g. "ctrl+s", "enter")."""
        result = self._session.press(keys)
        return {
            "success": result.success,
            "message": getattr(result, "message", ""),
            "error": getattr(result, "error", None),
        }

    def find(self, query: str | None = None, name: str | None = None, limit: int = 5) -> list[dict]:
        """트리에서 요소 시맨틱 검색."""
        return self._session.find(query=query, name=name, limit=limit)

    def open_app(self, name: str) -> dict:
        """앱 이름으로 실행 (fuzzy match)."""
        result = self._session.open_app(name)
        return {
            "success": result.success,
            "message": getattr(result, "message", ""),
            "error": getattr(result, "error", None),
        }
