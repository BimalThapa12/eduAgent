
import json
import re
import ollama

from config import OLLAMA_MODEL, OLLAMA_HOST


# Connect to local Ollama server
client = ollama.Client(host=OLLAMA_HOST)


RUBRIC = {
    "R1": "Technical accuracy",
    "R2": "Grounding in reference material",
    "R3": "Beginner friendliness",
    "R4": "Simple language",
    "R5": "Practical examples",
    "R6": "Topic coverage",
    "R7": "Teaching flow",
    "R8": "Standalone quality"
}


# --------------------------------------------------
# VALIDATE EVALUATION EVIDENCE
# --------------------------------------------------

def validate_evaluation_evidence(checks):

    generic_evidence = {
        "explanation of the decision",
        "the lesson meets the requirement",
        "this criterion is satisfied",
        "good explanation",
        "satisfactory",
        "meets the requirement",
        "the lesson is good"
    }

    for check in checks:

        evidence = check.get("evidence", "")

        if not isinstance(evidence, str) or len(evidence.strip()) < 20:

            check["status"] = "FAIL"

            check["feedback"] = (
                "Evaluator did not provide sufficient "
                "specific evidence."
            )

            continue

        normalized = evidence.strip().lower()

        if normalized in generic_evidence:

            check["status"] = "FAIL"

            check["feedback"] = (
                "Evaluator provided generic evidence "
                "instead of specific evidence from the lesson."
            )

    return checks


# --------------------------------------------------
# OLLAMA EVALUATION
# --------------------------------------------------

def evaluate_with_fallback(prompt):

    try:

        print(f"Evaluating with Ollama model: {OLLAMA_MODEL}")

        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict educational quality evaluator. "
                        "Return only valid JSON. Do not include Markdown."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json",
            options={
                "temperature": 0.1
            }
        )

        content = response["message"]["content"]

        if not content:
            raise ValueError("Ollama returned an empty evaluation.")

        return content

    except Exception as error:

        print(f"Ollama evaluation failed: {error}")

        raise RuntimeError(
            f"Local evaluation failed: {error}"
        ) from error


# --------------------------------------------------
# EVALUATE LESSON
# --------------------------------------------------

def evaluate_lesson(topic, lesson, reference_material):

    rubric_text = "\n".join(
        f"{key}: {value}"
        for key, value in RUBRIC.items()
    )

    prompt = f"""
You are an independent educational quality evaluator.

Evaluate the generated lesson strictly.

TOPIC:
{topic}

REFERENCE MATERIAL:
{reference_material}

GENERATED LESSON:
{lesson}

FIXED EVALUATION RUBRIC:
{rubric_text}

RULES:

1. Evaluate all eight checkpoints independently.
2. Each checkpoint must receive PASS or FAIL.
3. Never mark a missing requirement as PASS.
4. Technical claims must be accurate.
5. Check factual claims against the reference material.
6. Do not assume RAG guarantees 100% accuracy.
7. Do not assume RAG automatically guarantees privacy.
8. Give specific evidence quoted or accurately described
   from the generated lesson for every decision.
9. Generic evidence is not acceptable.
10. Give actionable feedback for every failed checkpoint.
11. Do not invent evidence.
12. Be strict and objective.

For example, useful evidence would be:
"The lesson defines RAG as Retrieval-Augmented Generation."

Unacceptable evidence would be:
"Explanation of the decision."

Return ONLY valid JSON in this format:

{{
    "checks": [
        {{
            "id": "R1",
            "name": "Technical accuracy",
            "status": "PASS",
            "evidence": "Specific evidence from the lesson",
            "feedback": ""
        }}
    ],
    "overall_feedback": "Summary of the evaluation",
    "approved": true
}}

IMPORTANT:
- Include exactly R1 through R8.
- Use only PASS or FAIL.
- approved must be true ONLY when all eight checks PASS.
- Every evidence field must describe something specific
  found in the generated lesson.
"""

    response_text = evaluate_with_fallback(prompt)

    # Remove accidental Markdown code fences
    clean_text = response_text.strip()

    clean_text = re.sub(
        r"^```(?:json)?\s*",
        "",
        clean_text,
        flags=re.IGNORECASE
    )

    clean_text = re.sub(
        r"\s*```$",
        "",
        clean_text
    )

    # Parse JSON
    try:

        result = json.loads(clean_text)

    except json.JSONDecodeError as error:

        raise ValueError(
            f"Evaluator returned invalid JSON: {error}"
        ) from error

    # Validate evaluator output
    checks = result.get("checks", [])

    if not isinstance(checks, list) or len(checks) != 8:

        raise ValueError(
            "Evaluator must return exactly eight checkpoints."
        )

    check_map = {
        check.get("id"): check
        for check in checks
        if isinstance(check, dict)
    }

    if len(check_map) != 8 or set(check_map) != set(RUBRIC):

        raise ValueError(
            "Evaluator must return exactly R1-R8 without duplicates."
        )

    # Validate each checkpoint
    for check_id in RUBRIC:

        check = check_map[check_id]

        if check.get("status") not in ["PASS", "FAIL"]:

            raise ValueError(
                f"Invalid status for {check_id}"
            )

        if not isinstance(check.get("evidence"), str):

            raise ValueError(
                f"Invalid evidence for {check_id}"
            )

        if check["status"] == "FAIL" and not check.get("feedback"):

            raise ValueError(
                f"Missing improvement feedback for {check_id}"
            )

        if check["status"] == "PASS":
            check["feedback"] = ""

    # Apply evidence validation
    checks = validate_evaluation_evidence(
        [check_map[rid] for rid in RUBRIC]
    )

    # Calculate approval locally.
    # Never trust the model's approval flag.
    result["approved"] = all(
        check["status"] == "PASS"
        for check in checks
    )

    result["checks"] = checks

    return result
