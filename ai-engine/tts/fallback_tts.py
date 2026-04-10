from typing import Callable, List


class TTSFallback:
    def __init__(self, providers: List[Callable[[str, str], str]]) -> None:
        self.providers = providers

    async def synthesize(self, text: str, voice: str) -> str:
        errors = []
        for provider in self.providers:
            try:
                return provider(text, voice)
            except Exception as exc:  # pragma: no cover - network provider fallback path
                errors.append(str(exc))
        raise RuntimeError(f"All TTS providers failed: {errors}")
