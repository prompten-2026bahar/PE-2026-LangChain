from __future__ import annotations

from pydantic import BaseModel, Field


class Issue(BaseModel):
    line: int = Field(..., ge=1)
    message: str
    suggestion: str


class ReviewResult(BaseModel):
    score: int = Field(..., ge=0, le=100)
    issues: list[Issue] = Field(default_factory=list)


class AnalyzeRequest(BaseModel):
    code: str = Field(..., min_length=1)


class BuildAttempt(BaseModel):
    attempt: int
    thought: str
    action: str
    observation: str
    code: str
    succeeded: bool = False


class SelfHealingRequest(BaseModel):
    code: str = Field(..., min_length=1)
    max_attempts: int = Field(default=3, ge=1, le=5)


class SelfHealingResponse(BaseModel):
    success: bool
    final_code: str
    attempts: list[BuildAttempt]
    summary: list[str] = Field(default_factory=list)
