import time

from farmer_helper.schemas.answering import (
    AnswerGenerationRequest,
    AnswerGenerationResponse,
    LLMGenerateRequest,
    LLMMessage,
    PromptBuildRequest,
)
from farmer_helper.schemas.session import FollowUpContextRequest
from farmer_helper.services.answering.citation_mapper import CitationMapper
from farmer_helper.services.answering.diagnostics_logger import AnswerDiagnosticsLogger
from farmer_helper.services.answering.prompt_builder import PromptBuilder
from farmer_helper.services.answering.provider import LLMProvider
from farmer_helper.services.performance.model_router import LLMModelRouter
from farmer_helper.services.session.context_resolver import FollowUpContextResolver


class AnswerGenerationService:
    def __init__(
        self,
        prompt_builder: PromptBuilder,
        provider: LLMProvider,
        citation_mapper: CitationMapper | None = None,
        diagnostics_logger: AnswerDiagnosticsLogger | None = None,
        context_resolver: FollowUpContextResolver | None = None,
        model_router: LLMModelRouter | None = None,
    ) -> None:
        """Init for answer-generation workflows.

        Initialize AnswerGenerationService for answer-generation workflows. Inputs are
        prompt_builder, provider, citation_mapper, diagnostics_logger, context_resolver,
        model_router. It runs synchronously and returns when local processing is complete. The
        operation is executed for its side effects and does not return a payload.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        self._prompt_builder = prompt_builder
        self._provider = provider
        self._citation_mapper = citation_mapper or CitationMapper()
        self._diagnostics_logger = diagnostics_logger or AnswerDiagnosticsLogger()
        self._context_resolver = context_resolver
        self._model_router = model_router or LLMModelRouter()

    def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
        """Generate for answer-generation workflows.

        This AnswerGenerationService method belongs to the answer-generation service layer.
        Inputs are request. It runs synchronously and returns when local processing is complete.
        Returns a AnswerGenerationResponse value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        start = time.perf_counter()
        effective_question = request.question
        if request.session_key and self._context_resolver is not None:
            context = self._context_resolver.resolve(
                FollowUpContextRequest(
                    session_key=request.session_key,
                    question=request.question,
                    max_messages=request.context_max_messages,
                    max_turns=request.context_max_turns,
                )
            )
            if context.context_text:
                effective_question = (
                    "Follow-up context:\n"
                    f"{context.context_text}\n\n"
                    "Current question:\n"
                    f"{request.question}"
                )

        prompt_result = self._prompt_builder.build(
            PromptBuildRequest(
                question=effective_question,
                retrieved_chunks=request.retrieved_chunks,
                max_chunks=request.max_chunks,
            )
        )
        selected_model = self._model_router.route(question=request.question)

        if prompt_result.decision == "refuse":
            total_ms = (time.perf_counter() - start) * 1000
            self._diagnostics_logger.generation_completed(
                decision="refuse",
                model=selected_model,
                citations_count=0,
                input_tokens=0,
                output_tokens=0,
                confidence=0.0,
                total_ms=total_ms,
            )
            return AnswerGenerationResponse(
                decision="refuse",
                refusal_reason=prompt_result.refusal_reason,
                refusal_code=prompt_result.refusal_code,
                clarification_message=None,
            )

        if prompt_result.decision == "clarify":
            total_ms = (time.perf_counter() - start) * 1000
            self._diagnostics_logger.generation_completed(
                decision="clarify",
                model=selected_model,
                citations_count=0,
                input_tokens=0,
                output_tokens=0,
                confidence=0.0,
                total_ms=total_ms,
            )
            return AnswerGenerationResponse(
                decision="clarify",
                clarification_message=prompt_result.clarification_message,
                clarification_code=prompt_result.clarification_code,
                refusal_reason=None,
            )

        llm_response = self._provider.generate(
            LLMGenerateRequest(
                model=selected_model,
                messages=[
                    LLMMessage(role="system", content=prompt_result.system_prompt),
                    LLMMessage(role="user", content=prompt_result.user_prompt),
                ],
                max_tokens=request.max_answer_tokens,
                temperature=request.temperature,
            )
        )

        citations = self._citation_mapper.map_citations(
            chunks=request.retrieved_chunks,
            max_citations=request.max_chunks,
        )

        total_ms = (time.perf_counter() - start) * 1000
        confidence = self._estimate_confidence(
            citations_count=len(citations),
            finish_reason=llm_response.finish_reason,
        )
        self._diagnostics_logger.generation_completed(
            decision="answer",
            model=llm_response.model,
            citations_count=len(citations),
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
            confidence=confidence,
            total_ms=total_ms,
        )

        return AnswerGenerationResponse(
            decision="answer",
            answer=llm_response.text,
            citations=citations,
            model=llm_response.model,
            finish_reason=llm_response.finish_reason,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
        )

    @staticmethod
    def _estimate_confidence(citations_count: int, finish_reason: str) -> float:
        """Estimate confidence for answer-generation workflows.

        This private helper belongs to the answer-generation service layer. Inputs are
        citations_count, finish_reason. It runs synchronously and returns when local processing
        is complete. Returns a float value that downstream API or orchestration layers can
        consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        confidence = min(1.0, 0.4 + (0.1 * citations_count))
        if finish_reason == "length":
            confidence = max(0.0, confidence - 0.1)
        return confidence
