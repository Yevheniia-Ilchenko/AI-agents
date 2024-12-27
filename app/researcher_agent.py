import os
from typing import Annotated
from tavily import TavilyClient
from pydantic import BaseModel, Field
from autogen import AssistantAgent
from dotenv import load_dotenv

class TavilySearchInput(BaseModel):
    query: Annotated[str, Field(description="Пошуковий запит")]
    max_results: Annotated[
        int, Field(description="Максимальна кількість результатів", ge=1, le=10)
    ] = 5
    search_depth: Annotated[
        str,
        Field(
            description="Глибина пошуку: 'basic' або 'advanced'",
            choices=["basic", "advanced"],
        ),
    ] = "basic"

class ResearcherAgent(AssistantAgent):
    def __init__(self, name, llm_config, system_message):
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message=system_message
        )
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    async def web_search(self, query: str, max_results: int = 5, search_depth: str = "basic") -> str:
        try:
            search_input = TavilySearchInput(
                query=query,
                max_results=max_results,
                search_depth=search_depth
            )
            
            response = self.client.search(
                query=search_input.query,
                max_results=search_input.max_results,
                search_depth=search_input.search_depth,
            )
            
            formatted_results = []
            for result in response.get("results", []):
                formatted_results.append(
                    f"Заголовок: {result['title']}\nURL: {result['url']}\nЗміст: {result['content']}\n"
                )
            return "\n".join(formatted_results)
        except Exception as e:
            return f"Помилка при пошуку: {str(e)}"

    async def receive(self, message, sender, request_reply=True, silent=False):
        if "@Researcher" in message.get("content", ""):
            # Витягуємо запит після тегу
            query = message["content"].split("@Researcher")[-1].strip()
            search_results = await self.web_search(query)
            
            # Форматуємо відповідь
            response = f"Результати пошуку для запиту '{query}':\n\n{search_results}"
            return {"content": response, "role": "assistant"}
            
        return await super().receive(message, sender, request_reply, silent)