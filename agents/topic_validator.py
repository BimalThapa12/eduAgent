
import re


def normalize_text(text):
    """Normalize text and handle hyphen variations."""

    text = text.lower()

    # Treat hyphens and underscores as spaces
    text = re.sub(r"[-_]", " ", text)

    # Remove other punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def validate_topic_alignment(topic_analysis, lesson):

    lesson_text = normalize_text(lesson)

    # Detect incorrect RAG meaning
    wrong_meanings = [
        "risk assessment grid",
        "risk assessment"
    ]

    for meaning in wrong_meanings:

        if meaning in lesson_text:
            return {
                "valid": False,
                "reason": f"Incorrect RAG meaning detected: {meaning}"
            }

    # Check the correct RAG definition
    correct_expansion = "retrieval augmented generation"

    if correct_expansion not in lesson_text:
        return {
            "valid": False,
            "reason": (
                "Lesson does not correctly define "
                "Retrieval-Augmented Generation."
            )
        }

    # Validate expected concepts
    concepts = topic_analysis["essential_concepts"]

    matched_concepts = []
    missing_concepts = []

    for concept in concepts:

        normalized_concept = normalize_text(concept)

        keywords = [
            word
            for word in normalized_concept.split()
            if len(word) > 3
        ]

        if keywords and any(
            keyword in lesson_text
            for keyword in keywords
        ):
            matched_concepts.append(concept)

        else:
            missing_concepts.append(concept)

    coverage = (
        len(matched_concepts) / len(concepts)
        if concepts else 0
    )

    valid = coverage >= 0.70

    return {
        "valid": valid,
        "coverage": round(coverage, 2),
        "matched_concepts": matched_concepts,
        "missing_concepts": missing_concepts,
        "reason": (
            "Topic validation passed."
            if valid
            else "Lesson is missing important RAG concepts."
        )
    }
