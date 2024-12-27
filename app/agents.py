from autogen.agentchat import UserProxyAgent,AssistantAgent,GroupChat,GroupChatManager
from dotenv import load_dotenv
load_dotenv()
from typing import Annotated
from prompts import CEO_PROMPT, CTO_PROMPT,  CFO_PROMPT, PLANNER_PROMPT, CRITIC_PROMPT, RESEARCHER_PROMPT
from config import get_gpt_config
from datetime import datetime
# from researcher_agent import ResearcherAgent
from autogen import register_function
# from autogen.agentchat.contrib.web_surfer import WebSurferAgent
from tavily import TavilyClient
from pydantic import BaseModel, Field
import os
import json

from typing import Literal, Sequence
import json
import os
from datetime import datetime
from tavily import TavilyClient

def tavily_search(
    query: str,
    search_depth: str = "advanced",
    max_results: int = 5
) -> str:
    print(f"\nВиконується пошуковий запит: {query}")
    
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # Отримуємо відповідь
        response = tavily_client.qna_search(
            query=query,
            search_depth=search_depth,
            max_results=max_results
        )
        
        print(f"Тип відповіді: {type(response)}")
        
        # Форматуємо відповідь
        formatted_results = f"""=== РЕЗУЛЬТАТИ ДОСЛІДЖЕННЯ ===
Запит: {query}

Знайдена інформація:
{response}
"""
        
        # Зберігаємо результати з унікальним ім'ям файлу
        save_search_results(query, {
            "response": response,
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, filename=None)  # None для автоматичної генерації імені
        
        return formatted_results

    except Exception as e:
        error_msg = f"Помилка при пошуку: {str(e)}"
        print(error_msg)
        return error_msg


# def tavily_search(
#     query: str,
#     search_depth: str = "basic",
#     max_results: int = 5
# ) -> str:
#     print(f"\nВиконується пошуковий запит: {query}")
    
#     try:
#         # Створюємо клієнт
#         tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
#         # Отримуємо контекст безпосередньо
#         context = tavily_client.get_search_context(
#             query=query,
#             search_depth=search_depth,
#             max_results=max_results
#         )
        
#         # Форматуємо відповідь
#         formatted_results = f"""=== РЕЗУЛЬТАТИ ДОСЛІДЖЕННЯ ===
# Запит: {query}

# {context}
# """
        # Зберігаємо результати
    #     save_search_results(query, {"context": context})
        
    #     return formatted_results

    # except Exception as e:
    #     error_msg = f"Помилка при пошуку: {str(e)}"
    #     print(error_msg)
    #     return error_msg

def save_search_results(query: str, results: dict, filename=None):
    """Зберігає результати пошуку у JSON файл"""
    try:
        # Створюємо директорію
        os.makedirs("saved_research", exist_ok=True)
        
        # Створюємо унікальне ім'я файлу для кожного пошуку
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_query = "".join(c for c in query[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"search_{safe_query}_{timestamp}.json"
        
        file_path = os.path.join("saved_research", filename)
        
        # Готуємо дані для збереження
        data = {
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "response": results.get('response', ''),  # Отримуємо відповідь з результатів
            "sources": results.get('sources', [])     # Додаємо джерела, якщо є
        }
        
        # Перевіряємо, чи існує файл
        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
                except json.JSONDecodeError:
                    existing_data = []
        
        # Додаємо нові дані
        existing_data.append(data)
        
        # Зберігаємо оновлений файл
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        
        print(f"\nРезультати збережено у: {file_path}")
        return file_path
        
    except Exception as e:
        print(f"Помилка при збереженні: {str(e)}")
        return None



# Функція для виконання пошуку
# def tavily_search(
#     query: str,
#     max_results: int = 5,
#     search_depth: str = "basic"
# ) -> str:
#     print(f"\nВиконується пошуковий запит: {query}")
    
#     client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
#     try:
#         response = client.search(
#             query=query,
#             max_results=max_results,
#             search_depth=search_depth,
#         )
        
#         # Збереження результатів у файл
#         save_search_results(query, response)
        
#         formatted_results = []
#         for result in response.get("results", []):
#             formatted_results.append(
#                 f"Заголовок: {result['title']}\nURL: {result['url']}\nЗміст: {result['content']}\n"
#             )
        
#         result_text = "\n".join(formatted_results)
#         print("\nПошук успішно виконано!")
#         return result_text
#     except Exception as e:
#         error_msg = f"Помилка при пошуку: {str(e)}"
#         print(error_msg)
#         return error_msg

# def save_search_results(query: str, results: dict, filename="research_results.json"):
#     """Зберігає результати пошуку у JSON файл"""
#     try:
#         # Створюємо директорію, якщо не існує
#         os.makedirs("saved_research", exist_ok=True)
#         file_path = os.path.join("saved_research", filename)
        
#         # Форматуємо дані для збереження
#         data_to_save = {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "results": [
#                 {
#                     "title": item['title'],
#                     "url": item['url'],
#                     "content": item['content']
#                 }
#                 for item in results.get('results', [])
#             ]
#         }
        
#         # Зберігаємо у файл
#         with open(file_path, "w", encoding="utf-8") as file:
#             json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        
#         print(f"\nРезультати збережено у: {file_path}")
        
#     except Exception as e:
#         print(f"Помилка при збереженні: {str(e)}")

def is_termination_message(message):
    """
    Визначає, чи сигналізує повідомлення про завершення роботи агентів.
    """
    return "TERMINATE" in message.get("content", "").upper()


def create_agents(gpt_config=None):

  if gpt_config is None:
      gpt_config = get_gpt_config()

  code_execution_config = {"last_n_messages": 15,
    "work_dir": "research_workspace",
    "use_docker": False,
    "timeout": 60,
    "stream_output": True}
  
  os.makedirs(code_execution_config["work_dir"], exist_ok=True)

  # User Proxy Agent  CEO
  ceo = UserProxyAgent( 
      name="CEO",  
      human_input_mode="ALWAYS",  
      system_message=CEO_PROMPT,
      code_execution_config= False,  
      llm_config=gpt_config,  
      description="""Call this Agent if:   
          You need strategic leadership and decision-making for your startup.
          You need to oversee the project's progress and ensure timely completion.
          You need to allocate resources effectively.
          DO NOT CALL THIS AGENT IF:  
          You need to perform specific technical tasks.""",  
  )

  # Planner — координатор
  planner = AssistantAgent(
    name="Planner",
    llm_config=gpt_config,
    system_message=PLANNER_PROMPT,
    description="""Call this Agent if:
        You need to split tasks among CFO, CTO, Critic
        You want to store summary and chat logs
        and deliver final results back to CEO.
    """
)
  # Додаємо метод send_message до Planner
  def send_message(self, message):
        # Додаємо повідомлення до списку messages
        if not hasattr(self, "messages"):
            self.messages = []  # Ініціалізуємо, якщо messages не існує
        self.messages.append(message)
        print(f"{self.name} надіслав повідомлення:\n{message}")

  from types import MethodType
  planner.send_message = MethodType(send_message, planner)

  # Assistant Agent -   CTO
  cto = AssistantAgent(
      name="CTO",
      llm_config=gpt_config,
      system_message= CTO_PROMPT,
      is_termination_msg=is_termination_message,
      description="""Call this Agent if:
            You need technical design, planning, architecture, risk assessment.   
.
  """
  )
  # Assistant Agent - CFO
  cfo = AssistantAgent(
      name="CFO",
      llm_config=gpt_config,
      system_message=CFO_PROMPT,
      is_termination_msg=is_termination_message,
      description="""Call this Agent if:   
          You need financial analysis, budgeting, risk evaluation
          You need to control and optimize expenses.
          You need to assess and mitigate financial risks.
"""
  )  
    
  #  Assistant Agent - Critic
  critic = AssistantAgent(
        name="Critic",
        llm_config=gpt_config,
        system_message=CRITIC_PROMPT,
        is_termination_msg=is_termination_message,
        description="""Call this Agent if:
            You want an analytical review of responses from CTO and CFO 
            to ensure their decisions align with project objectives and mitigate risks.
            
            TRIGGER CONDITIONS:
            - Call this agent only after both CTO and CFO have provided their responses to the Planner's request.
            - Ensure the input contains summaries or direct content from CTO and CFO for analysis.

            DO NOT CALL THIS AGENT IF: 
            - This is the first request from the Planner.
            - Responses from CTO or CFO are missing or incomplete.
            
            KEY OBJECTIVE:
            - Provide constructive analysis and critique of the provided technical and financial plans.
            - Highlight potential risks and offer actionable recommendations for improvement.
        
        """
    )


  researcher = AssistantAgent(
        name="Researcher",
        system_message=RESEARCHER_PROMPT,
        llm_config=gpt_config,
        description="""Call this Agent if:
           You need additional market/technical/financial data or trends and oyjer agents call @Researcher.
         """,
        code_execution_config=code_execution_config
    )
  register_function(
        tavily_search,
        caller=researcher,
        executor=researcher,
        name="tavily_search",
        description="Пошук інформації в інтернеті через Tavily API"
    )
    
    # Також можемо зареєструвати для інших агентів, якщо потрібно
#   for agent in [cfo, cto, planner]:
#         agent.code_execution_config = code_execution_config





  allowed_transitions = {
        ceo: [planner, researcher],
        planner: [ cfo, cto, critic, ceo],
        cfo: [planner, cto, critic, researcher],
        cto: [planner, cfo, critic, researcher],
        critic: [planner, cfo, cto],
        researcher: [ceo, cfo, cto, planner]
    }


  system_message_manager = """You are the manager of a collaborative team.
    Ensure proper communication flow between CTO and CFO.
    When you see @Researcher tag, make sure to pass the message to Researcher agent.
    Activate Critic only after both CFO and CTO have provided their responses.
    Guide the conversation to achieve concrete results.
       """
  groupchat = GroupChat(
      agents=[ceo, planner, cfo, cto, critic, researcher],
      allowed_or_disallowed_speaker_transitions=allowed_transitions,
      speaker_transitions_type="allowed",
      messages=[],
      max_round=20,
      send_introductions=True,
      speaker_selection_method="auto"
  )


  manager = GroupChatManager(groupchat=groupchat, llm_config=gpt_config, system_message=system_message_manager)
  return ceo,planner, manager, researcher


