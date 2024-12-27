from autogen.agentchat import UserProxyAgent, AssistantAgent, ConversableAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
load_dotenv()
import os
from autogen.cache import Cache


config_list_gpt = [{"model": "gpt-3.5-turbo", "api_key": os.getenv('OPENAI_API_KEY')}]

gpt_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list_gpt,
    "timeout": 120,
    "max_tokens": 2000,
}

ceo_agent = UserProxyAgent(
    name="CEO",
    code_execution_config=False,
    system_message="Lead discussions, assign tasks to CFO and CTO, and provide feedback.",
    llm_config=gpt_config,  # Використовує GPT для автоматизації, якщо потрібно
    # description="""Call this Agent if:   
    #       You need strategic leadership and decision-making for your startup.
    #       You need to oversee the project's progress and ensure timely completion.
    #       You need to allocate resources effectively.
    #       DO NOT CALL THIS AGENT IF:  
    #       You need to perform specific technical tasks.""",
    human_input_mode="ALWAYS" # Завжди запитувати ввід від користувача
)



cto_agent = AssistantAgent(
    name="CTO",

    description="Responsible for technical strategy and infrastructure planning.",
    llm_config=gpt_config
)


cfo_agent = ConversableAgent(
    name="CFO",
    system_message="Analyze financial data, generate forecasts, and evaluate budgets.",
    description="Handles financial responsibilities and provides insights.",
    llm_config=gpt_config
)

critic = AssistantAgent(
    name="Critic",
    system_message="""Critic. Аналізуй плани, які пропонуються іншими агентами. Став питання для уточнення або вказуй на потенційні проблеми. Твоя мета — зробити обговорення більш точним та вичерпним.""",
    llm_config=gpt_config,
)

# Створення групового чату з агентами
group_chat = GroupChat(
    agents=[ceo_agent, cto_agent, cfo_agent, critic],
    max_round=50,send_introductions=True, messages=[]  # Максимальна кількість раундів обговорення
)

# Менеджер чату
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=gpt_config,  # Модель для обговорення
)

# Запуск чату
task = "Discuss the company's strategy for next quarter, including technical and financial aspects."
with Cache.disk(cache_seed=1) as cache:
    chat_result=ceo_agent.initiate_chat(
        manager,
        message=task
    , clear_history=True
    )

print(chat_result.cost)