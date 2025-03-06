import openai
from pydantic import BaseModel
from typing import Optional

class OpenRouterRequest(BaseModel):
    prompt: str
    model: str = "liquid/lfm-7b"  # Модель по умолчанию
    max_tokens: Optional[int] = 500
    temperature: Optional[float] = 0.7

class OpenRouterResponse(BaseModel):
    response: str
    status: str

class OpenRouterIntegration:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key
        self.base_url = base_url

        # Настройка OpenAI клиента для работы с OpenRouter
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    async def generate_response(self, request: OpenRouterRequest) -> OpenRouterResponse:
        try:
            # Отправка запроса к OpenRouter
            completion = await self.client.completions.create(
                model=request.model,
                prompt=request.prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )

            # Извлечение текста ответа
            response_text = completion.choices[0].text.strip()
            return OpenRouterResponse(response=response_text, status="success")

        except Exception as e:
            # Обработка ошибок
            return OpenRouterResponse(response=str(e), status="error")