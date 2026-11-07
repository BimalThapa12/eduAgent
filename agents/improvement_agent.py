def create_improvement_instructions(evaluation):

    checks = evaluation.get("checks", [])

    failed_checks = [
        check for check in checks
        if check["status"] == "FAIL"
    ]

    if not failed_checks:
        return "No improvements required. All quality checks passed."

    instructions = []

    instructions.append(
        "Improve the previous lesson using the following feedback:"
    )

    for check in failed_checks:

        checkpoint_id = check["id"]
        checkpoint_name = check["name"]
        evidence = check["evidence"]
        feedback = check["feedback"]

        instructions.append(
            f"""
Checkpoint: {checkpoint_id} - {checkpoint_name}

Problem identified:
{evidence}

Required improvement:
{feedback}
"""
        )

    instructions.append(
        """
IMPORTANT:
1. Fix every identified issue.
2. Preserve all technically correct explanations.
3. Keep the language beginner-friendly.
4. Do not remove important learning concepts.
5. Do not ignore any failed checkpoint.
6. Do not weaken the evaluation standards.
"""
    )

    return "\n".join(instructions)