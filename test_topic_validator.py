from pathlib import Path

from agents.topic_analyzer import analyze_topic
from agents.topic_validator import validate_topic_alignment

reference = Path(
    "knowledge/rag_reference.md"
).read_text(encoding="utf-8")

analysis = analyze_topic(
    topic="Introduction to RAG",
    student_level="12th-grade graduate",
    reference_material=reference
)


good_lesson = """
Retrieval-Augmented Generation (RAG) is an AI technique
that combines information retrieval with text generation.

Retrieval finds relevant information from external
knowledge sources. Generation uses the retrieved
information to create an answer using a Large Language Model.

How RAG Works:
Documents are collected and divided into smaller sections
called chunks. Embeddings convert text into numerical
representations. These embeddings are stored in a searchable
vector database. When a user asks a question, the system
retrieves relevant document chunks and provides them as
context to the language model.

RAG vs Traditional LLM:
A traditional LLM generally uses information learned
during training and supplied prompt context. RAG retrieves
additional information from external sources before
generating its answer.

Benefits:
RAG can use organization-specific documents and updated
knowledge without retraining the entire language model.

Limitations:
RAG does not guarantee correct answers. Its quality
depends on source documents, retrieval, and generation.
"""


bad_lesson = """
RAG stands for Risk Assessment Grid.
It helps businesses identify and prioritize risks.
"""

print("GOOD LESSON:")
print(
    validate_topic_alignment(analysis, good_lesson)
)

print("\nBAD LESSON:")
print(
    validate_topic_alignment(analysis, bad_lesson)
)