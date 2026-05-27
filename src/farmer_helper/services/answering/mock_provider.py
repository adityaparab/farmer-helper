from farmer_helper.schemas.answering import LLMGenerateRequest, LLMGenerateResponse
from farmer_helper.services.answering.provider import LLMProvider


class MockLLMProvider(LLMProvider):
    def generate(self, request: LLMGenerateRequest) -> LLMGenerateResponse:
        user_message = next(
            (message.content for message in request.messages if message.role == "user"),
            "",
        )
        text = (
            "Based on the provided context, prioritize soil organic matter, "
            "mulching, and irrigation scheduling."
        )
        if "insufficient" in user_message.lower():
            text = "The provided context is insufficient to provide a grounded answer."

        return LLMGenerateResponse(
            model=request.model,
            text=text,
            finish_reason="stop",
            input_tokens=max(1, len(user_message.split())),
            output_tokens=max(1, len(text.split())),
        )
