
import json
import ollama

from config import OLLAMA_MODEL, OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)


def analyze_topic(topic, student_level, reference_material):

    prompt = f"""
You are an educational topic analyzer.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

REFERENCE MATERIAL:
{reference_material}

Identify the essential learning requirements for
an introductory lesson about Retrieval-Augmented Generation.

Use the reference material as your source.

Return exactly these five essential concepts:

1. Definition of Retrieval-Augmented Generation.
2. Retrieval and generation.
3. The RAG workflow, including document processing,
   chunking, embeddings, storage and retrieval.
4. RAG compared with a traditional LLM.
5. Benefits and limitations of RAG.

Do not change, merge, or remove these five concepts.

Also identify common misunderstandings.

Return valid JSON only:

{{
    "topic": "Introduction to RAG",
    "correct_definition": "Definition from reference material",
    "essential_concepts": [
        "Definition of Retrieval-Augmented Generation",
        "Retrieval and generation",
        "RAG workflow",
        "RAG compared with traditional LLM",
        "Benefits and limitations of RAG"
    ],
    "common_misunderstandings": [
        "RAG guarantees correct answers"
    ]
}}
"""

    try:
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json",
            options={"temperature": 0}
        )

        result = json.loads(
            response["message"]["content"]
        )

        required = [
            "topic",
            "correct_definition",
            "essential_concepts",
            "common_misunderstandings"
        ]

        for field in required:
            if field not in result:
                raise ValueError(f"Missing field: {field}")

        if len(result["essential_concepts"]) != 5:
            raise ValueError("Expected exactly five concepts.")

        return result

    except Exception as error:
        raise RuntimeError(
            f"Topic analysis failed: {error}"
        ) from error
