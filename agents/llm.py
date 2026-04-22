'''
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(user_prompt: str):
    # ✅ Fix encoding issue
    with open("prompts/finance.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
'''

from groq import Groq
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Get API key safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Check your .env file or environment variables.")

# ✅ Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_response(user_prompt: str):
    try:
        # ✅ Load system prompt safely
        with open("prompts/finance.md", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # ✅ Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        # ✅ Proper error handling (important for your benchmark script)
        return f"❌ LLM Error: {str(e)}"