from pathlib import Path
from agents.generator import generate_with_fallback

# Load reference material
reference_path = Path("knowledge/rag_reference.md")
reference_material = reference_path.read_text(encoding="utf-8")

prompt = f"""
Explain Retrieval-Augmented Generation (RAG)
to a student who has just completed 12th grade.

Use the following reference material:

{reference_material}

Requirements:
1. Use simple English.
2. Explain retrieval and generation separately.
3. Explain the RAG workflow step by step.
4. Include a college handbook example.
5. Explain at least two limitations.
6. Make the lesson standalone.
"""

lesson = generate_with_fallback(
    prompt,
    task_name="Reference-Based Generation"
)

print("\n========== GENERATED LESSON ==========\n")
print(lesson)