import os
import streamlit as st
from datetime import datetime
import json


def save_chat_history_to_file(chat_history, filename="chat_history.txt"):
    
    abs_dir_path = os.path.abspath("saved_chat")
    os.makedirs(abs_dir_path, exist_ok=True)
    
    # Створюємо шлях до файлу
    file_path = os.path.join(abs_dir_path, filename)
    
    
    with open(file_path, "a", encoding="utf-8") as file:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Chat - Date and Time: {time}\n")
        for message in chat_history:
            
            content = message.get("content", "")
            agent_name = message.get("name", "")
            file.write(f"\n\n Agent: {agent_name}\nContent: {content}\n\n")

    return file_path



def save_chat_history_from_session_to_file(chat_history, filename="chat_history.txt"):
    """
    Зберігає історію чату у файл.
    chat_history: рядок (str), що містить повну історію чату.
    """

    # Переконайтеся, що chat_history не пустий
    if not chat_history:
        st.write("Увага: Історія чату порожня, файл буде пустим.")

    abs_dir_path = os.path.abspath("saved_chat")
    os.makedirs(abs_dir_path, exist_ok=True)

    file_path = os.path.join(abs_dir_path, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(chat_history)
        return file_path
    except Exception as e:
        st.write(f"Помилка при збереженні файла: {e}")
        return None
    

def load_summary_from_file(filename="summary.json"):
    """
    Завантажує саммарі з файлу у форматі JSON.
    """
    file_path = os.path.abspath(f"saved_chat/{filename}")
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            summary = json.load(file)
        return summary
    else:
        return None
    

def provide_summary_to_agents(planner, summary_file="summary.json"):
    """
    Завантажує саммарі з файлу у вигляді JSON і додає до контексту через Planner.
    """
    file_path = os.path.abspath(f"saved_chat/{summary_file}")

    # Перевіряємо, чи існує файл
    if not os.path.exists(file_path):
        print("Файл саммарі не знайдено. Саммарі не було додано до контексту.")
        return

    # Завантажуємо саммарі з файлу
    with open(file_path, "r", encoding="utf-8") as file:
        summary_data = json.load(file)
    
    # Отримуємо текст саммарі
    summary_content = summary_data.get("summary", "Саммарі відсутнє.")

    # Формуємо повідомлення
    message = (
        "\n Додаємо попереднє саммарі до контексту:\n\n"
        f"{summary_content}\n\n"
        "Будь ласка, врахуйте ці дані у своїх наступних відповідях.\n"
    )
    
    # Надсилаємо повідомлення через Planner
    if hasattr(planner, "send_message"):
        planner.send_message(message)
        print("Саммарі було успішно надіслано через Planner.\n")
    else:
        print("Planner не має методу send_message. Саммарі не було надіслано.")
