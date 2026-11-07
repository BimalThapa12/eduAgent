from agents.generator import (
    generate_lesson,
    regenerate_lesson
)

from agents.improvement_agent import (
    create_improvement_instructions
)

topic = "Introduction to RAG"

student_level = (
    "12th-grade graduate with limited English vocabulary"
)

# Generate initial lesson
lesson = generate_lesson(
    topic,
    "S1",
    student_level
)

# Simulate evaluator feedback
evaluation = {
    "checks": [
        {
            "id": "R1",
            "name": "Technical accuracy",
            "status": "FAIL",
            "evidence": "The lesson claims RAG guarantees 100% accuracy.",
            "feedback": "Explain that RAG can reduce errors but cannot guarantee perfect accuracy."
        },
        {
            "id": "R2",
            "name": "Grounding",
            "status": "PASS",
            "evidence": "Claims are supported.",
            "feedback": ""
        }
    ]
}

# Create improvement instructions
instructions = create_improvement_instructions(evaluation)

# Regenerate lesson
improved_lesson = regenerate_lesson(
    topic,
    "S1",
    student_level,
    lesson,
    instructions
)

print("\n========== IMPROVED LESSON ==========\n")
print(improved_lesson)