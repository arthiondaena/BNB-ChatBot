import streamlit as st
from openai import OpenAI
from collections import deque
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(layout="wide")

# Load knowledge base
@st.cache_data
def load_knowledge():
    with open("bingenbash.md", "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge()

# Session state for chat history and API settings
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = deque(maxlen=10)  # 5 user-assistant pairs

st.title("Binge N Bash Customer Support Chatbot")

# Sidebar config
st.sidebar.header("OpenAI API Settings")
api_key = st.sidebar.text_input("API Key", type="password", value=os.environ.get("OPENROUTER_API_KEY", ""))
base_url = st.sidebar.text_input("Base URL", value="https://openrouter.ai/api/v1")

model = "meta-llama/llama-3.3-70b-instruct:free"

if api_key and base_url:
    client = OpenAI(api_key=api_key, base_url=base_url)

    # Main chat interface
    user_input = st.chat_input("Ask a question about support...")

    if user_input:
        def build_messages(user_input):
            system_prompt = (
                "You are a helpful customer support assistant. "
                "Use the following knowledge base to answer questions accurately and clearly."
                "Refuse to answer any question that isn't related to the knowledge base."
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Knowledge Base:\n{knowledge}"}
            ]

            messages.extend(st.session_state.conversation_history)
            messages.append({"role": "user", "content": user_input})
            return messages

        with st.spinner("Thinking..."):
            try:
                messages = build_messages(user_input)
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.5,
                )
                assistant_reply = response.choices[0].message.content

                # Store history
                st.session_state.conversation_history.append({"role": "user", "content": user_input})
                st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                assistant_reply = f"Error: {e}"

    # Display chat messages
    for msg in st.session_state.conversation_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

else:
    st.warning("Please enter your OpenAI API key and base url in the sidebar to start chatting.")
