import os
import logging

from openai import OpenAI
from dotenv import load_dotenv
from collections import deque
from translate import translate_text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

load_dotenv()

model = "meta-llama/llama-3.3-70b-instruct:free"

# Load knowledge base
with open("bingenbash.md", "r", encoding="utf-8") as f:
    knowledge = f.read()

# Initialize conversation history (keep last 5 exchanges)
conversation_history = deque(maxlen=10)  # 5 user-assistant pairs = 10 messages

def build_prompt(user_input):
    system_prompt = (
        "You are a helpful customer support assistant. "
        "Use the following knowledge base to answer questions accurately and clearly."
    )
    messages = [{"role": "system", "content": system_prompt},
                {"role": "system", "content": f"Knowledge Base:\n{knowledge}"}]

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_input})
    return messages

def ask_chatbot(client, user_input):
    global conversation_history

    messages = build_prompt(user_input)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )

    assistant_reply = response.choices[0].message.content

    # Update conversation history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply

def main():
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('translate-api-python.json')

    print("Customer Support Chatbot (type 'exit' to quit)")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        user_input = translate_text(user_input, credentials=credentials)
        reply = ask_chatbot(client, user_input)
        print(f"Bot: {reply}")

if __name__ == "__main__":
    main()
