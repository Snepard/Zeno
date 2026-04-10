from typing import Callable, List


class LLMFallbackClient:
    def __init__(self, providers: List[Callable[[str], str]]) -> None:
        self.providers = providers

    async def generate(self, prompt: str) -> str:
        errors = []
        for provider in self.providers:
            try:
                return provider(prompt)
            except Exception as exc:  # pragma: no cover - network provider fallback path
                errors.append(str(exc))
        raise RuntimeError(f"All LLM providers failed: {errors}")
