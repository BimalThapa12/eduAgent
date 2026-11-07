import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider
AI_PROVIDER = "ollama"

# Ollama configuration
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_HOST = "http://localhost:11434"

# Workflow configuration
MAX_RETRIES = 2