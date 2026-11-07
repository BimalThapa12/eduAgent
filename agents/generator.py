
import ollama
import config


# --------------------------------------------------
# OLLAMA STREAMING GENERATION
# --------------------------------------------------

def generate_with_fallback(prompt, task_name="Lesson Generation"):
    """
    Generate content using Ollama.
    Stream generated tokens directly to the terminal.
    Return the complete generated content.
    """

    try:
        print("\n" + "=" * 65, flush=True)
        print(f"EDUAGENT | {task_name}", flush=True)
        print("=" * 65 + "\n", flush=True)

        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True,
            options={
                "temperature": 0.7
            }
        )

        generated_content = []

        for chunk in response:

            content = chunk.get("message", {}).get("content", "")

            if content:
                print(content, end="", flush=True)
                generated_content.append(content)

        print("\n\n" + "=" * 65, flush=True)
        print("GENERATION COMPLETED", flush=True)
        print("=" * 65 + "\n", flush=True)

        result = "".join(generated_content)

        if not result.strip():
            raise ValueError("Ollama returned empty content.")

        return result

    except Exception as error:
        print(f"\nOllama generation failed: {error}", flush=True)
        raise


# --------------------------------------------------
# INITIAL LESSON GENERATION
# --------------------------------------------------

def generate_lesson(
    topic,
    strategy_id,
    student_level,
    reference_material="",
    topic_analysis=None
):
    """
    Generate the initial lesson.
    """

    topic_requirements = ""

    if topic_analysis:
        topic_requirements = f"""
TOPIC REQUIREMENTS:
{topic_analysis}

Follow these requirements carefully.
"""

    prompt = f"""
You are EduAgent AI, an expert educational content creator.

YOUR TASK:
Create a complete beginner-friendly lesson.

TOPIC:
{topic}

TARGET STUDENT:
{student_level}

GENERATION STRATEGY:
{strategy_id}

REFERENCE MATERIAL:
{reference_material}

{topic_requirements}

IMPORTANT INSTRUCTIONS:

1. Explain the topic using simple English.
2. Assume the student has limited technical knowledge.
3. Explain technical terms before using them.
4. Use short sentences and paragraphs.
5. Include practical, familiar examples.
6. Follow a logical teaching sequence.
7. Do not invent unsupported facts.
8. Use the supplied reference material as the source of truth.
9. Make the lesson understandable without requiring external resources.

FOR THE TOPIC INTRODUCTION TO RAG:

- Define RAG as Retrieval-Augmented Generation.
- Explain retrieval and generation.
- Explain the RAG workflow:
  document collection, processing, chunking, embeddings,
  storage, query processing, retrieval, context construction,
  and answer generation.
- Explain how RAG differs from a traditional LLM.
- Explain benefits and limitations.
- Include a practical example.
- Explain important terms in simple English.

NEVER confuse Retrieval-Augmented Generation with Risk Assessment Grid.

LESSON STRUCTURE:

# Introduction to the Topic

# What Is RAG?

# Why Is RAG Needed?

# How Does RAG Work?

# Important Concepts

# Practical Example

# RAG vs Traditional LLM

# Benefits of RAG

# Limitations of RAG

# Summary

# Quick Knowledge Check

Create a complete standalone lesson.
Do not include evaluator scores or internal workflow information.
"""

    return generate_with_fallback(
        prompt,
        task_name="INITIAL LESSON GENERATION"
    )


# --------------------------------------------------
# LESSON REGENERATION
# --------------------------------------------------

def regenerate_lesson(
    topic,
    strategy_id,
    student_level,
    previous_lesson,
    improvement_instructions,
    reference_material="",
    topic_analysis=None
):
    """
    Regenerate the lesson using evaluator feedback.
    """

    topic_requirements = ""

    if topic_analysis:
        topic_requirements = f"""
TOPIC REQUIREMENTS:
{topic_analysis}

Follow these requirements carefully.
"""

    prompt = f"""
You are EduAgent AI.

You previously generated a lesson, but the evaluator
identified mistakes that must be corrected.

TOPIC:
{topic}

TARGET STUDENT:
{student_level}

GENERATION STRATEGY:
{strategy_id}

REFERENCE MATERIAL:
{reference_material}

{topic_requirements}

PREVIOUS LESSON:
{previous_lesson}

EVALUATOR FEEDBACK AND IMPROVEMENT INSTRUCTIONS:
{improvement_instructions}

YOUR TASK:

1. Read the previous lesson carefully.
2. Understand every failed evaluation requirement.
3. Correct the identified mistakes.
4. Preserve sections that were already correct.
5. Use simple English suitable for the target student.
6. Explain technical terms with familiar examples.
7. Follow the supplied reference material.
8. Do not introduce new unsupported information.
9. Ensure the lesson remains complete and standalone.

IMPORTANT:

- Do not ignore evaluator feedback.
- Do not repeat the same mistakes.
- Do not remove correct explanations unnecessarily.
- Do not confuse Retrieval-Augmented Generation
  with Risk Assessment Grid.

Return the complete corrected lesson.

Do not provide a list of changes.
Do not include internal evaluation information.
"""

    return generate_with_fallback(
        prompt,
        task_name="LESSON REGENERATION"
    )
