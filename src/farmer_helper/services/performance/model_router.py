from farmer_helper.core.config import get_settings


class LLMModelRouter:
    def route(self, *, request_model: str, question: str) -> str:
        if request_model != "auto":
            return request_model

        settings = get_settings()
        if len(question.strip()) <= settings.llm_model_router_question_length_threshold:
            return settings.llm_model_low_cost
        return settings.llm_model_high_quality
