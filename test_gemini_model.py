from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("\nAvailable Gemini models:\n")

for model in client.models.list():
    print("Model:", model.name)
    print("Display name:", model.display_name)
    print("-" * 40)