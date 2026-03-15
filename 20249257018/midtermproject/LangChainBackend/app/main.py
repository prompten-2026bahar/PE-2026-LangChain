from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.agents.self_heal import run_self_healing_workflow
from app.chains.review import build_review_chain
from app.models import AnalyzeRequest, ReviewResult, SelfHealingRequest, SelfHealingResponse

app = FastAPI(title="Swift Analysis and Self-Healing API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=ReviewResult)
async def analyze_code(request: AnalyzeRequest) -> ReviewResult:
    try:
        chain, _ = build_review_chain()
        return await chain.ainvoke({"code": request.code})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/self-heal", response_model=SelfHealingResponse)
async def self_heal(request: SelfHealingRequest) -> SelfHealingResponse:
    try:
        return await run_self_healing_workflow(
            code=request.code,
            max_attempts=request.max_attempts,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.websocket("/ws/self-heal")
async def self_heal_stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        payload = json.loads(await websocket.receive_text())
        request = SelfHealingRequest(**payload)

        async def emit(event: dict) -> None:
            await websocket.send_json(event)

        response = await run_self_healing_workflow(
            code=request.code,
            max_attempts=request.max_attempts,
            event_callback=emit,
        )
        await websocket.send_json({"type": "done", "result": response.model_dump()})
    except WebSocketDisconnect:
        return
    except Exception as exc:
        await websocket.send_json(
            {
                "type": "error",
                "message": str(exc),
            }
        )
        await websocket.close(code=1011, reason="self-heal-failed")
