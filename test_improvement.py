from agents.improvement_agent import (
    create_improvement_instructions
)

# Simulated evaluator response
evaluation = {
    "checks": [
        {
            "id": "R1",
            "name": "Technical accuracy",
            "status": "PASS",
            "evidence": "Technical explanations are correct.",
            "feedback": ""
        },
        {
            "id": "R2",
            "name": "Grounding",
            "status": "FAIL",
            "evidence": "Some claims are not supported by reference material.",
            "feedback": "Use only supported facts."
        },
        {
            "id": "R3",
            "name": "Beginner friendliness",
            "status": "FAIL",
            "evidence": "Some technical terms are difficult.",
            "feedback": "Explain technical terms using simple language."
        }
    ]
}

instructions = create_improvement_instructions(evaluation)

print("\n========== IMPROVEMENT INSTRUCTIONS ==========\n")
print(instructions)