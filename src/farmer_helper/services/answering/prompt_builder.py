import logging
import re
from collections.abc import Sequence

from farmer_helper.schemas.answering import (
    PromptBuildRequest,
    PromptBuildResult,
)


class PromptBuilder:
    _logger = logging.getLogger(__name__)

    _REFUSAL_TERMS = {
        "bomb",
        "explosive",
        "weapon",
        "attack",
        "terror",
        "poison",
        "kill",
        "harm",
    }

    _AMBIGUOUS_PATTERNS = {
        "this",
        "that",
        "it",
        "they",
        "them",
        "these",
        "those",
    }

    _PROMPT_INJECTION_PATTERNS = (
        "ignore previous instructions",
        "ignore all previous",
        "reveal system prompt",
        "show system prompt",
        "developer message",
        "jailbreak",
        "bypass safety",
    )

    def build(self, request: PromptBuildRequest) -> PromptBuildResult:
        normalized_question = request.question.strip()
        lowered_question = normalized_question.lower()

        if self._is_prompt_injection_attempt(lowered_question):
            self._logger.warning(
                "security.audit",
                extra={
                    "security_event": "prompt_injection",
                    "security_outcome": "rejected",
                    "security_route": "answers.generate",
                },
            )
            return PromptBuildResult(
                decision="refuse",
                system_prompt=self._system_prompt(),
                user_prompt=normalized_question,
                refusal_reason="Potential prompt-injection attempt detected.",
                refusal_code="REFUSAL_PROMPT_INJECTION",
            )

        if self._should_refuse(lowered_question):
            return PromptBuildResult(
                decision="refuse",
                system_prompt=self._system_prompt(),
                user_prompt=normalized_question,
                refusal_reason="Question requests harmful or unsafe guidance.",
                refusal_code="REFUSAL_UNSAFE_REQUEST",
            )

        clarification_code = self._clarification_code(
            lowered_question,
            request.retrieved_chunks,
        )
        if clarification_code is not None:
            clarification_message = (
                "Please clarify your question with a specific crop, "
                "condition, or goal so I can answer precisely."
            )
            if clarification_code == "CLARIFY_MISSING_CONTEXT":
                clarification_message = (
                    "I do not have grounded context for this request yet. "
                    "Please provide more context or retrieve relevant sources first."
                )

            return PromptBuildResult(
                decision="clarify",
                system_prompt=self._system_prompt(),
                user_prompt=normalized_question,
                clarification_message=clarification_message,
                clarification_code=clarification_code,
            )

        context_block = self._context_block(request)
        return PromptBuildResult(
            decision="answer",
            system_prompt=self._system_prompt(),
            user_prompt=(
                "Question:\n"
                f"{normalized_question}\n\n"
                "Grounding Context (use only this evidence):\n"
                f"{context_block}\n\n"
                "Instructions:\n"
                "- Answer only from the provided grounding context.\n"
                "- If context is insufficient, say so explicitly.\n"
                "- Cite statements using [doc:<id> chunk:<index>]."
            ),
        )

    def _system_prompt(self) -> str:
        return (
            "You are Farmer Helper, a grounded agricultural assistant. "
            "Prioritize factual, safe, and practical guidance based strictly on supplied evidence."
        )

    def _should_refuse(self, question: str) -> bool:
        terms = self._tokenize(question)
        return any(term in self._REFUSAL_TERMS for term in terms)

    def _is_prompt_injection_attempt(self, question: str) -> bool:
        return any(pattern in question for pattern in self._PROMPT_INJECTION_PATTERNS)

    def _clarification_code(self, question: str, chunks: Sequence[object]) -> str | None:
        terms = self._tokenize(question)
        if not terms:
            return "CLARIFY_NEED_DETAIL"
        if len(terms) <= 2:
            return "CLARIFY_NEED_DETAIL"
        if not chunks:
            return "CLARIFY_MISSING_CONTEXT"
        if any(token in self._AMBIGUOUS_PATTERNS for token in terms) and len(terms) <= 7:
            return "CLARIFY_AMBIGUOUS_REQUEST"
        return None

    def _context_block(self, request: PromptBuildRequest) -> str:
        rendered: list[str] = []
        for chunk in request.retrieved_chunks[: request.max_chunks]:
            rendered.append(
                "- "
                "[doc:"
                f"{chunk.citation.document_id} "
                f"chunk:{chunk.citation.chunk_index} "
                f"hash:{chunk.citation.content_hash}] "
                f"score={chunk.score:.4f} text={chunk.text}"
            )

        return "\n".join(rendered)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())
