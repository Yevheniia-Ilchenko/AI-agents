import os
from dotenv import load_dotenv

# Завантаження змінних середовища з файлу .env
load_dotenv()

def get_gpt_config(temperature=0.0, max_tokens=1024, timeout=120, cache_seed=42):
    """
    Повертає конфігурацію GPT на основі заданих параметрів.
    """
    config_list_gpt = [{"model": "gpt-4o-mini", "api_key": os.getenv('OPENAI_API_KEY')}]

    return {
        "cache_seed": cache_seed,  # змініть cache_seed для різних проб
        "temperature": temperature,
        "config_list": config_list_gpt,
        "timeout": timeout,
        "max_tokens": max_tokens,
    }


# gpt_config = {
#     "cache_seed": 42,  # change the cache_seed for different trials
#     "temperature": 0,
#     "config_list": config_list_gpt,
#     "timeout": 120,
#     "max_tokens": 1024,
# }



# import os
# import logging
# from dotenv import load_dotenv

# # Налаштування логування
# logging.basicConfig(
#     level=logging.INFO,  # Записувати повідомлення рівня INFO та вище
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     filename="gpt_connection.log",  # Логи зберігатимуться у файлі
#     filemode="a",  # Додавати нові записи до файлу
# )

# logger = logging.getLogger("GPT_Config")  # Іменований логгер для вашого коду

# # Завантаження змінних середовища з файлу .env
# load_dotenv()

# def get_gpt_config(temperature=0.0, max_tokens=1024, timeout=120, cache_seed=42):
#     """
#     Повертає конфігурацію GPT на основі заданих параметрів.
#     """
#     api_key = os.getenv('OPENAI_API_KEY')

#     # Логування статусу API-ключа
#     if api_key:
#         logger.info("OPENAI_API_KEY successfully loaded from environment.")
#     else:
#         logger.error("OPENAI_API_KEY is missing. Check your .env file.")

#     # Формування конфігурації
#     config_list_gpt = [{"model": "gpt-3.5-turbo", "api_key": api_key}]
#     logger.info(f"GPT configuration created with temperature={temperature}, max_tokens={max_tokens}.")

#     return {
#         "cache_seed": cache_seed,  # змініть cache_seed для різних проб
#         "temperature": temperature,
#         "config_list": config_list_gpt,
#         "timeout": timeout,
#         "max_tokens": max_tokens,
#     }