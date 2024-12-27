
import streamlit as st
from manage_file import save_chat_history_to_file, save_chat_history_from_session_to_file
from io import StringIO
from agents import create_agents
from config import get_gpt_config

def run_streamlit():
    st.title("Agents Team")
    st.sidebar.header("GPT Config")

    # Створення слайдерів для налаштування конфігурації GPT
    temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.0)
    max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=4096, value=1024)
    timeout = st.sidebar.slider("Timeout", min_value=10, max_value=300, value=120)
    cache_seed = st.sidebar.slider("Cache Seed", min_value=0, max_value=300, value=42)

    # Отримання оновленої конфігурації GPT
    gpt_config = get_gpt_config(temperature, max_tokens, timeout, cache_seed)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""  # Історія всієї переписки
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = False
    if 'chat_result' not in st.session_state:
        st.session_state.chat_result = None
    if 'ceo' not in st.session_state or 'manager' not in st.session_state:
        st.session_state.ceo, st.session_state.manager = create_agents(gpt_config)
        st.session_state.conversation_active = True

    ceo = st.session_state.ceo
    manager = st.session_state.manager
    

    if st.sidebar.button("Apply new config"):
      st.session_state.ceo, st.session_state.manager = create_agents(gpt_config)
      st.success("Agents recreated with new config!")

    st.write("### Введіть завдання для чат-бота:")
    task1 = st.text_area("Task", """Розпишіть план та структуру створення чат-бота для допомоги дропхантерам за 2 місяці та бюджетом $20,000.
    Необхідно забезпечити швидкий запуск MVP, ефективне використання бюджету, чіткі KPI та координацію команди.
    Потрібно:
    1. Технічне рішення
    2. План розробки
    3. Бюджетування
    4. Оцінка ризиків""")

    if st.button("Run Task"):
        with st.spinner("Processing..."):
            chat_result = ceo.initiate_chat(
                manager,
                message=task1,
                clear_history=True
            )


            st.session_state.chat_result = chat_result
            st.session_state.chat_history += f"User: {task1}\n"
            history_str = ""
            for msg in chat_result.chat_history:
              agent_name = msg.get("name", "")
              content = msg.get("content", "")
              history_str += f"Agent: {agent_name}\nContent: {content}\n\n"
            st.session_state.chat_history += f"Agents:\n{history_str}\n"

        
    if st.session_state.chat_result:
      chat_result = st.session_state.chat_result
      st.write("### Повна історія чату:")
      if hasattr(chat_result, 'chat_history'):
          history_str = ""
          for msg in chat_result.chat_history:
              agent_name = msg.get("name", "")
              content = msg.get("content", "")
              history_str += f"Agent: {agent_name}\nContent: {content}\n\n"
        
          st.text_area("Chat History", history_str, height=300)
      else:
        st.write("Немає повідомлень у історії.")

        
      st.write("### Вартість чату:")
      st.write(f"Вартість: {chat_result.cost['usage_including_cached_inference']}")

      if st.button("Save Chat to File"):
        st.write("Спроба збереження чату...")
        file_path = save_chat_history_from_session_to_file(st.session_state.chat_history)
        if file_path:
            st.success("Chat history saved successfully!")
            st.write(f"Збережено в файл: {file_path}")
      else:
        st.error("Не вдалося зберегти історію чату.")


if __name__ == "__main__":
    run_streamlit()