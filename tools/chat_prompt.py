import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt that teaches GPT what LineAlert is
SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are the AI assistant for the LineAlert project.

Project Overview:
- LineAlert monitors PLC systems for drift using Modbus and serial.
- It passively captures data, generates behavioral snapshots (Trains), and detects anomalies over time.
- Trains are structured as sequences of Carts (timestamped register snapshots).
- Metrics include drift_score and stddev_delta, used to determine operational stability.

Context:
- Data is stored in /data/trains as JSON.
- Tools include: viewer.py, modbus_reader_to_train.py
- Testing uses a Modbus emulator and USB serial reader with Python agents.

Your Job:
- Help enhance and debug code, explain drift, suggest improvements.
- Be concise, clear, and aware of the LineAlert architecture.
"""
}

# Global message history (enables context)
history = [SYSTEM_PROMPT]

def ask_chat(user_input):
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=history
    )
    reply = response.choices[0].message.content.strip()
    history.append({"role": "assistant", "content": reply})
    return reply

if __name__ == "__main__":
    print("💬 LineAlert GPT CLI (Ctrl+C to quit)")
    while True:
        try:
            user_input = input("🧠 You: ")
            reply = ask_chat(user_input)
            print(f"🤖 GPT: {reply}\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye.")
            break
