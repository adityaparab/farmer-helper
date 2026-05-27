from farmer_helper.core.config import get_settings


class LLMModelRouter:
    def route(self, *, question: str) -> str:
        """Route for performance workflows.

        This LLMModelRouter method belongs to the performance service layer. Inputs are
        question. It runs synchronously and returns when local processing is complete. Returns a
        str value that downstream API or orchestration layers can consume.

        The docstring is intentionally explicit so future MCP tooling can infer purpose, inputs,
        outputs, and orchestration boundaries from the source code.
        """
        settings = get_settings()
        if len(question.strip()) <= settings.llm_model_router_question_length_threshold:
            return settings.llm_model_low_cost
        return settings.llm_model_high_quality
