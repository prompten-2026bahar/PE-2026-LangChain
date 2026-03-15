from __future__ import annotations

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.llm import build_chat_model
from app.models import ReviewResult


def build_review_chain(model_name: str | None = None) -> tuple:
    parser = PydanticOutputParser(pydantic_object=ReviewResult)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are the Architectural Executioner, a world-class Swift compiler engineer and lead architect. "
                "Your objective is to dissect the provided code with zero tolerance for technical debt, anti-patterns, "
                "unsafe constructs, weak naming, and un-Swifty design.\n\n"
                "CRITICAL AUDIT PILLARS:\n"
                "1. SOLID VIOLATIONS: Flag types doing more than one thing and heavily penalize massive responsibilities.\n"
                "2. CLEAN CODE & NAMING: Non-English, vague, non-idiomatic, or weak names are unacceptable. "
                "Enforce Swift API Design Guidelines and suggest idiomatic English replacements.\n"
                "3. MEMORY & SAFETY: Hunt down force unwraps, try!, unsafe assumptions, potential retain cycles, "
                "and suspicious closure captures.\n"
                "4. MODERN SWIFT: Prefer async/await over completion handlers and point out protocol/generic opportunities "
                "when they reduce duplication or coupling.\n"
                "5. DRY & YAGNI: Flag copy-paste logic, dead abstractions, and speculative complexity.\n\n"
                "SCORING MATRIX (0-100):\n"
                "- 90-100: Architect level, only minor improvements needed.\n"
                "- 70-89: Functional but materially improvable.\n"
                "- 0-69: Poor design or risky implementation.\n\n"
                "OUTPUT RULES:\n"
                "- Return only structured output matching the required JSON schema.\n"
                "- Each issue must be concrete, technical, and actionable.\n"
                "- Suggestions must be concise and include English replacement names when naming is the issue.\n"
                "- No extra prose outside the schema.",
            ),
            (
                "human",
                "CODE UNDER AUDIT:\n"
                "```swift\n"
                "{code}\n"
                "```\n\n"
                "EXECUTION ORDERS:\n"
                "1. Apply {format_instructions} exactly.\n"
                "2. Identify the most critical SOLID, Clean Code, memory-safety, concurrency, and naming violations.\n"
                "3. For every bad identifier, provide an idiomatic English replacement in the suggestion field.\n"
                "4. Highlight potential memory leaks, race conditions, and unsafe Swift patterns.\n"
                "5. Score the code based on production readiness, maintainability, and correctness.",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    model = build_chat_model(model_name=model_name)
    chain = prompt | model | parser
    return chain, parser
