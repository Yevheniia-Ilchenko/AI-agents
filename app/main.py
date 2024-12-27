from agents import create_agents
from manage_file import save_chat_history_to_file, provide_summary_to_agents, load_summary_from_file
from config import get_gpt_config
import os

from datetime import datetime
import json


def save_summary_to_file(task, summary, filename="summary.json"):
    os.makedirs("saved_chat", exist_ok=True)
    file_path = os.path.join("saved_chat", filename)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", encoding="utf-8") as file:
        json.dump({
            "task": task,
            "date": time,
            "summary": summary
        }, file, ensure_ascii=False, indent=4)
    print(f"Саммарі збережено у файл: {file_path}")


def main():

    gpt_config = get_gpt_config()

    ceo, planner,  manager, researcher = create_agents(gpt_config)


    task = """


    Розпишіть план та структуру створення чат-бота для допомоги дропхантерам на 2 місяці,
    з бюджетом $20,000. Потрібні:
    1. Технічне рішення (CTO)
    2. План розробки (Planner)
    3. Бюджетування (CFO)
    4. Оцінка ризиків (Critic)

    @Researcher знайди інформацію які краще технології використовувати для СТО та як краще бюджетувати для СФО,щоб надати більше деталей та актуальної інформації на грудень 2024 
   

    Завершуйте відповіді лише конкретними діями або результатами.
    """

    # Ініціація чату через CEOAgent
    chat_result = ceo.initiate_chat(
        manager,
        message=task,
        clear_history=True,
        summary_method="reflection_with_llm"
    )


    # Збереження історії чату у файл
    create_file = save_chat_history_to_file(chat_result.chat_history)

    save_summary_to_file( chat_result.summary, task)

    # Виведення результатів
    print("Результати обговорення:")
    print(chat_result.summary)
    print("\nЗбережено в файл:", create_file)
    print("\nВартість:", chat_result.cost)

if __name__ == "__main__":
    main()

# def main():
#     # subprocess.run(["streamlit", "run", "ui.py"])

   
#    ceo, manager = create_agents()

#    task1 = ""


#    chat_result=ceo.initiate_chat(
#       manager,
#       message=task1
#   , clear_history=True
#   )
   
#    create_file = save_chat_history_to_file(chat_result.chat_history)

#    print("Результати обговорення:")
#    print(chat_result.summary)
#    print("Збережено в файл:", create_file)
#    print("\nВартість:", chat_result.cost)

# if __name__ == "__main__":
#     main()

