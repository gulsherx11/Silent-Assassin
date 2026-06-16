import os
import pyperclip
import keyboard
from dotenv import load_dotenv

from openai import OpenAI
import google.generativeai as genai

load_dotenv()

# ==========================
# OPENROUTER
# ==========================

openrouter = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

OPENROUTER_MODEL = "openrouter/free"

# ==========================
# GEMINI
# ==========================

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================
# GROQ
# ==========================

groq = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

GROQ_MODEL = "llama-3.3-70b-versatile"


# ==========================
# PROVIDERS
# ==========================

def ask_openrouter(prompt):
    response = openrouter.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def ask_gemini(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text


def ask_groq(prompt):
    response = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ==========================
# FALLBACK CHAIN
# ==========================

def ask_ai(prompt):

    try:
        print("Trying OpenRouter...")
        answer = ask_openrouter(prompt)
        print("✓ OpenRouter")
        return answer

    except Exception as e:
        print("OpenRouter failed:", e)

    try:
        print("Trying Gemini...")
        answer = ask_gemini(prompt)
        print("✓ Gemini")
        return answer

    except Exception as e:
        print("Gemini failed:", e)

    try:
        print("Trying Groq...")
        answer = ask_groq(prompt)
        print("✓ Groq")
        return answer

    except Exception as e:
        print("Groq failed:", e)

    return "ERROR: All providers failed."


# ==========================
# HOTKEY ACTION
# ==========================

def generate():

    text = pyperclip.paste().strip()

    if not text:
        print("Clipboard is empty.")
        return

    print(f"Processing {len(text)} characters...")

    answer = ask_ai(text)

    pyperclip.copy(answer)

    print("Response copied to clipboard.")


# Change this to any hotkey you prefer
keyboard.add_hotkey("ctrl+alt+a", generate)

print("--------------------------------")
print("AI Clipboard Assistant Running")
print("ctrl+alt+a")
print("--------------------------------")

keyboard.wait()