import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

class imput_hlper():
    def top_line():
        parser = argparse.ArgumentParser(description="AI Code Assistant")
        parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
        args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
     