
from reinforcement.reward import calculate_reward


evaluation = {
    "checks": [
        {"id": "R1", "status": "PASS"},
        {"id": "R2", "status": "PASS"},
        {"id": "R3", "status": "PASS"},
        {"id": "R4", "status": "PASS"},
        {"id": "R5", "status": "PASS"},
        {"id": "R6", "status": "PASS"},
        {"id": "R7", "status": "PASS"},
        {"id": "R8", "status": "PASS"}
    ]
}

reward = calculate_reward(evaluation)

print("Evaluation completed!")
print("Calculated reward:", reward)
