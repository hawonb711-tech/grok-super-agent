"""REST API server for the agentic autonomous system."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agent import ReActAgent

app = FastAPI(
    title="Grok Super Agent API",
    description="멀티 AI 오케스트레이션 + Computer Use — x.ai/Tesla ecosystem",
    version="0.2.0",
)


class TaskRequest(BaseModel):
    """Request body for task execution."""

    task: str
    decompose: bool = False


class TaskResponse(BaseModel):
    """Response body for task execution."""

    result: str


@app.get("/")
def root() -> dict:
    """Health check."""
    return {"status": "ok", "service": "grok-super-agent"}


@app.post("/task", response_model=TaskResponse)
def run_task(req: TaskRequest) -> TaskResponse:
    """Execute a task via the ReAct agent."""
    try:
        agent = ReActAgent()
        result = agent.run(req.task)
        return TaskResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")


@app.post("/computer-use", response_model=TaskResponse)
def run_computer_use(req: TaskRequest) -> TaskResponse:
    """Execute a task via Computer Use + 멀티 AI 오케스트레이터."""
    try:
        from src.orchestrator.loop import ComputerUseLoop

        loop = ComputerUseLoop()
        result = loop.run(req.task, decompose=req.decompose)
        return TaskResponse(result=result)
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Computer Use not available: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Computer Use error: {e}")
