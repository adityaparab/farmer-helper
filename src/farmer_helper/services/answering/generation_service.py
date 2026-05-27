from farmer_helper.schemas.answering import (
    AnswerGenerationRequest,
    AnswerGenerationResponse,
    Citation,
    LLMGenerateRequest,
    LLMMessage,
    PromptBuildRequest,
)
from farmer_helper.services.answering.prompt_builder import PromptBuilder
from farmer_helper.services.answering.provider import LLMProvider


class AnswerGenerationService:
    def __init__(self, prompt_builder: PromptBuilder, provider: LLMProvider) -> None:
        self._prompt_builder = prompt_builder
        self._provider = provider

    def generate(self, request: AnswerGenerationRequest) -> AnswerGenerationResponse:
        prompt_result = self._prompt_builder.build(
            PromptBuildRequest(
                question=request.question,
                retrieved_chunks=request.retrieved_chunks,
                max_chunks=request.max_chunks,
            )
        )

        if prompt_result.decision == "refuse":
            return AnswerGenerationResponse(
                decision="refuse",
                refusal_reason=prompt_result.refusal_reason,
                clarification_message=None,
            )

        if prompt_result.decision == "clarify":
            return AnswerGenerationResponse(
                decision="clarify",
                clarification_message=prompt_result.clarification_message,
                refusal_reason=None,
            )

        llm_response = self._provider.generate(
            LLMGenerateRequest(
                model=request.model,
                messages=[
                    LLMMessage(role="system", content=prompt_result.system_prompt),
                    LLMMessage(role="user", content=prompt_result.user_prompt),
                ],
                max_tokens=request.max_answer_tokens,
                temperature=request.temperature,
            )
        )

        citations = [
            Citation(
                document_id=chunk.citation.document_id,
                chunk_index=chunk.citation.chunk_index,
                content_hash=chunk.citation.content_hash,
            )
            for chunk in request.retrieved_chunks[: request.max_chunks]
        ]

        return AnswerGenerationResponse(
            decision="answer",
            answer=llm_response.text,
            citations=citations,
            model=llm_response.model,
            finish_reason=llm_response.finish_reason,
            input_tokens=llm_response.input_tokens,
            output_tokens=llm_response.output_tokens,
        )
