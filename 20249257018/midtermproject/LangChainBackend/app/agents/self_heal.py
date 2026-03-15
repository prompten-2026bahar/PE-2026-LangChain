from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any

from langchain.agents import create_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.llm import build_chat_model
from app.models import BuildAttempt, SelfHealingResponse


class SwiftBuildInput(BaseModel):
    code: str = Field(..., description="Complete Swift source code to compile.")
    filename: str = Field(
        default="Main.swift",
        description="Temporary Swift source filename used during compilation.",
    )


class ChangeSummary(BaseModel):
    summary: list[str] = Field(
        default_factory=list,
        description="Concise bullet points describing the code changes and their impact.",
    )


IOS_FRAMEWORK_IMPORTS = {
    "UIKit",
    "WatchKit",
    "WidgetKit",
    "RealityKit",
}


def requires_ios_sdk(code: str) -> bool:
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped.startswith("import "):
            continue
        module_name = stripped.removeprefix("import ").split()[0]
        if module_name in IOS_FRAMEWORK_IMPORTS:
            return True
    return False


def compiler_command(source_path: Path, code: str) -> tuple[list[str], str]:
    if requires_ios_sdk(code):
        return (
            [
                "xcrun",
                "--sdk",
                "iphonesimulator",
                "swiftc",
                "-typecheck",
                "-target",
                "arm64-apple-ios18.0-simulator",
                str(source_path),
            ],
            "Typecheck (iOS Simulator SDK)",
        )
    return (
        [
            "swiftc",
            "-typecheck",
            str(source_path),
        ],
        "Typecheck (local Swift toolchain)",
    )


def swift_build_tool(code: str, filename: str = "Main.swift") -> str:
    if not code.strip():
        return "BUILD FAILED\nNo Swift source was provided to the compiler."

    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = Path(temp_dir) / filename
        source_path.write_text(code, encoding="utf-8")
        command, mode = compiler_command(source_path, code)

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )
        output = (process.stdout or "") + (process.stderr or "")
        status = "BUILD SUCCEEDED" if process.returncode == 0 else "BUILD FAILED"
        details = output.strip()
        if details:
            return f"{status}\nBuild Mode: {mode}\n{details}".strip()
        return f"{status}\nBuild Mode: {mode}"


def make_build_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=swift_build_tool,
        name="SwiftBuildTool",
        description=(
            "Compiles Swift source code with swiftc. "
            "Use it after refactoring Swift code and inspect compiler output carefully."
        ),
        args_schema=SwiftBuildInput,
    )


def build_self_healing_agent(model_name: str | None = None):
    model = build_chat_model(model_name=model_name)
    return create_agent(
        model=model,
        tools=[make_build_tool()],
        system_prompt=(
            "You are an autonomous Swift refactoring agent. "
            "Refactor Swift code, use SwiftBuildTool when needed, inspect compiler feedback, "
            "and return only the full corrected Swift source in the final answer. "
            "Apply Clean Code principles aggressively: use clear English names for all identifiers, "
            "remove debug prints, reduce side effects, prefer small focused APIs, and preserve behavior. "
            "Do not delete platform frameworks such as UIKit just to force a successful build. "
            "Preserve the intended Apple platform unless compiler feedback proves the code is fundamentally invalid."
        ),
    )


def extract_final_code(result: dict[str, Any]) -> str:
    messages = result.get("messages", [])
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            content = message.content
            if isinstance(content, str):
                return sanitize_swift_output(content)
            if isinstance(content, list):
                text_parts = [
                    part.get("text", "").strip()
                    for part in content
                    if isinstance(part, dict) and part.get("type") == "text"
                ]
                return sanitize_swift_output("\n".join(part for part in text_parts if part))
    raise ValueError("Agent did not return final Swift code.")


def sanitize_swift_output(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def format_attempt_prompt(code: str, prior_observations: list[str], attempt: int) -> str:
    history = "\n\n".join(
        f"Previous compiler feedback #{index + 1}:\n{observation}"
        for index, observation in enumerate(prior_observations)
    )
    return (
        f"Attempt {attempt} of 3.\n"
        "Fix and build this Swift code. Use SwiftBuildTool before producing the final answer.\n"
        "Avoid repeating previous compiler mistakes.\n"
        "If identifiers are non-English, translate them into idiomatic English while preserving behavior.\n"
        "Prefer clean code, descriptive naming, and simple structure.\n\n"
        f"{history}\n\n"
        f"Current Swift code:\n```swift\n{code}\n```"
    )


async def summarize_changes(
    original_code: str,
    final_code: str,
    attempts: list[BuildAttempt],
    succeeded: bool,
    model_name: str | None = None,
) -> list[str]:
    parser = PydanticOutputParser(pydantic_object=ChangeSummary)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You summarize Swift refactors for a developer dashboard. "
                "Be concrete, short, and technical. Mention naming cleanups, logic fixes, "
                "structural cleanup, and any remaining problems. Return only the required schema.",
            ),
            (
                "human",
                "Summarize what changed between the original Swift code and the final Swift code.\n"
                "If non-English identifiers were translated, mention that explicitly.\n"
                "If the build still fails, say what remains unresolved.\n"
                "{format_instructions}\n\n"
                "Build succeeded: {succeeded}\n"
                "Attempt count: {attempt_count}\n\n"
                "Original code:\n```swift\n{original_code}\n```\n\n"
                "Final code:\n```swift\n{final_code}\n```\n\n"
                "Compiler observations:\n{observations}",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    observations = "\n\n".join(
        f"Attempt {attempt.attempt}: {attempt.observation}" for attempt in attempts
    )
    model = build_chat_model(model_name=model_name)
    chain = prompt | model | parser

    try:
        result = await chain.ainvoke(
            {
                "original_code": original_code,
                "final_code": final_code,
                "observations": observations,
                "succeeded": succeeded,
                "attempt_count": len(attempts),
            }
        )
        return result.summary
    except Exception:
        fallback = []
        if succeeded:
            fallback.append("Build errors were resolved and the final Swift code compiles successfully.")
        else:
            fallback.append("The agent applied refactors, but the final version still has unresolved build issues.")
        if original_code != final_code:
            fallback.append("The code structure and naming were updated to improve readability and maintainability.")
        if attempts:
            fallback.append(f"The workflow completed in {len(attempts)} attempt(s).")
        return fallback


async def run_self_healing_workflow(
    code: str,
    max_attempts: int = 3,
    model_name: str | None = None,
    event_callback=None,
) -> SelfHealingResponse:
    original_code = code
    current_code = code
    attempts: list[BuildAttempt] = []
    prior_observations: list[str] = []
    agent = build_self_healing_agent(model_name=model_name)

    for attempt in range(1, max_attempts + 1):
        thought = f"Attempt {attempt}: refactor the Swift source and compile it."
        if event_callback:
            await event_callback(
                {
                    "type": "thought",
                    "attempt": attempt,
                    "message": thought,
                }
            )

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": format_attempt_prompt(current_code, prior_observations, attempt),
                    }
                ]
            }
        )
        final_code = extract_final_code(result)
        if not final_code.strip():
            final_code = current_code
            observation = (
                "BUILD FAILED\n"
                "The agent returned empty Swift source. Return the complete corrected file."
            )
        else:
            observation = swift_build_tool(final_code)
        succeeded = observation.startswith("BUILD SUCCEEDED")
        prior_observations.append(observation)

        build_attempt = BuildAttempt(
            attempt=attempt,
            thought=thought,
            action="SwiftBuildTool",
            observation=observation,
            code=final_code,
            succeeded=succeeded,
        )
        attempts.append(build_attempt)
        current_code = final_code

        if event_callback:
            await event_callback(
                {
                    "type": "observation",
                    "attempt": attempt,
                    "message": observation,
                    "succeeded": succeeded,
                    "code": final_code,
                }
            )

        if succeeded:
            summary = await summarize_changes(
                original_code=original_code,
                final_code=current_code,
                attempts=attempts,
                succeeded=True,
                model_name=model_name,
            )
            return SelfHealingResponse(
                success=True,
                final_code=current_code,
                attempts=attempts,
                summary=summary,
            )

    summary = await summarize_changes(
        original_code=original_code,
        final_code=current_code,
        attempts=attempts,
        succeeded=False,
        model_name=model_name,
    )
    return SelfHealingResponse(
        success=False,
        final_code=current_code,
        attempts=attempts,
        summary=summary,
    )
