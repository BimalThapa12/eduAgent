
# EduAgent AI - Reward Calculator

# Importance of each evaluation checkpoint
REWARD_WEIGHTS = {
    "R1": 3,  # Technical accuracy
    "R2": 2,  # Grounding
    "R3": 2,  # Beginner friendliness
    "R4": 2,  # Simple language
    "R5": 2,  # Practical examples
    "R6": 2,  # Topic coverage
    "R7": 1,  # Teaching flow
    "R8": 1   # Standalone quality
}


def calculate_reward(evaluation):

    checks = evaluation.get("checks", [])

    # Convert the evaluation results into a dictionary
    check_map = {
        check["id"]: check
        for check in checks
    }

    # Check whether all eight checkpoints are present
    if set(check_map.keys()) != set(REWARD_WEIGHTS.keys()):
        raise ValueError("Missing or invalid evaluation checkpoints")

    score = 0

    # Calculate weighted score
    for checkpoint, weight in REWARD_WEIGHTS.items():

        status = check_map[checkpoint]["status"]

        if status == "PASS":
            score += weight

        elif status != "FAIL":
            raise ValueError(f"Invalid status for {checkpoint}")

    # Give bonus only when all checkpoints pass
    all_passed = all(
        check_map[rid]["status"] == "PASS"
        for rid in REWARD_WEIGHTS
    )

    approval_bonus = 5 if all_passed else 0

    # Normalize reward between 0 and 1
    reward = (score + approval_bonus) / 20

    return round(reward, 4)
