# EduAgent AI – Setup and Installation Guide

This guide explains how to install, configure, and run EduAgent AI locally.

EduAgent AI is a self-evaluating educational content generation system built using Python, LangGraph, Ollama, Llama 3.2, and SQLite.

---

## 1. Prerequisites

Before setting up the project, make sure the following software is installed.

| Software | Purpose |
|---|---|
| Python 3.9+ | Application development |
| Git | Repository cloning |
| Ollama | Local language model execution |
| Visual Studio Code | Code editor |
| Terminal | Running commands |

### Download the required software

- Python: https://www.python.org/downloads/
- Git: https://git-scm.com/downloads
- Ollama: https://ollama.com/
- VS Code: https://code.visualstudio.com/

---

## 2. Clone the Repository

Open your terminal and navigate to the directory where you want to store the project.

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd eduAgent
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

---

## 3. Install Project Dependencies

Make sure you are inside the project directory.

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs the Python dependencies required by EduAgent.

If you use `python3`, you can also run:

```bash
python3 -m pip install -r requirements.txt
```

---

## 4. Install and Configure Ollama

EduAgent uses Ollama to run its language model locally.

### Step 1: Install Ollama

Download and install Ollama:

https://ollama.com/

### Step 2: Download the Model

Open the terminal and execute:

```bash
ollama pull llama3.2:3b
```

This downloads the Llama 3.2 3B model.

### Step 3: Verify the Installation

Run:

```bash
ollama list
```

You should see the downloaded model in the list.

### Step 4: Verify Ollama

Run:

```bash
ollama run llama3.2:3b
```

Enter a simple question to verify that the model responds.

Exit the Ollama session when finished.

Ollama must be running locally before starting EduAgent.

---

## 5. Configure the Application

Open the project in Visual Studio Code.

The application configuration is maintained in:

```text
config.py
```

The current configuration is:

```python
import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = "ollama"
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_HOST = "http://localhost:11434"
MAX_RETRIES = 2
```

### Configuration Explanation

| Setting | Description |
|---|---|
| AI_PROVIDER | Selects Ollama as the LLM provider |
| OLLAMA_MODEL | Specifies the model used by EduAgent |
| OLLAMA_HOST | Local Ollama server address |
| MAX_RETRIES | Maximum number of regeneration attempts |

The current configuration uses local Ollama execution and does not require a Gemini API key.

---

## 6. Verify the Reference Material

EduAgent uses reference material to ground its educational content.

Navigate to:

```text
knowledge/rag_reference.md
```

Make sure the file exists and contains the required learning material.

---

## 7. Verify the Project Structure

```text
eduAgent/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── agents/
├── workflow/
├── memory/
├── knowledge/
├── prompts/
├── reinforcement/
├── utils/
│
├── outputs/
│   ├── lessons/
│   └── evaluation_logs/
│
└── logs/
```

---

## 8. Run EduAgent AI

Make sure Ollama is running.

Execute:

```bash
python3 main.py
```

On Windows:

```bash
python main.py
```

The workflow will start automatically:

1. Select a generation strategy.
2. Analyze the requested topic.
3. Generate the initial lesson.
4. Validate topic alignment.
5. Evaluate the lesson against R1–R8.
6. Generate improvement instructions if evaluation fails.
7. Regenerate the lesson within the retry limit.
8. Approve or reject the final lesson.
9. Calculate the reward and update strategy performance.
10. Save the lesson and evaluation results.

The actual Ollama-generated content appears progressively in the terminal through streaming.

---

## 9. Access Generated Outputs

| Output | Location | Format |
|---|---|---|
| Approved lessons | `outputs/lessons/` | Markdown |
| Evaluation results | `outputs/evaluation_logs/` | JSON |
| Workflow logs | `logs/` | TXT |
| Persistent memory | `memory/eduagent.db` | SQLite |

---

## 10. Troubleshooting

### Ollama connection refused

Start Ollama:

```bash
ollama serve
```

### Model not found

Download the model:

```bash
ollama pull llama3.2:3b
```

### Python module not found

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Graph compilation error

Run:

```bash
python3 -c "from workflow.graph import eduagent_graph; print('Graph compiled successfully!')"
```

### Generated lesson is rejected

Check the evaluation JSON in:

```text
outputs/evaluation_logs/
```

Review the failed criteria and evaluator feedback.

---

## 11. Important Notes

- Python and Ollama must be installed.
- The `llama3.2:3b` model must be downloaded before execution.
- Ollama must be running locally.
- Reference material must be available in the knowledge directory.
- SQLite stores persistent learning information.
- EduAgent uses feedback-driven regeneration and strategy selection; it does not fine-tune the underlying Llama model.
- The current demonstration is configured for Introduction to RAG.

---

## 12. Quick Start

For users who already have Python, Git, and Ollama installed:

```bash
# Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL

# Navigate into the project
cd eduAgent

# Install dependencies
pip install -r requirements.txt

# Download the LLM
ollama pull llama3.2:3b

# Run EduAgent
python3 main.py
```

**EduAgent AI is now ready to generate, evaluate, and improve educational lessons locally.**