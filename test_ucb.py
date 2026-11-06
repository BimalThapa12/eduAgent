
from reinforcement.strategy_selector import (
    initialize_strategy_stats,
    select_strategy,
    calculate_ucb
)

# Initialize strategies
stats = initialize_strategy_stats()

print("Initial strategy statistics:")
print(stats)

print("\nTesting UCB selection:")

# First five selections should explore all strategies.
for i in range(5):

    selected = select_strategy(stats)

    print(f"Selection {i + 1}: {selected}")

    # Simulate a reward for testing.
    reward = {
        "S1": 0.60,
        "S2": 0.80,
        "S3": 0.45,
        "S4": 0.70,
        "S5": 0.90
    }[selected]

    stats[selected]["count"] += 1

    stats[selected]["total_reward"] += reward

    stats[selected]["average_reward"] = (
        stats[selected]["total_reward"]
        / stats[selected]["count"]
    )


print("\nUpdated statistics:")

for strategy_id, data in stats.items():

    print(
        strategy_id,
        "Count:", data["count"],
        "Average reward:", round(data["average_reward"], 2)
    )


# Select the next strategy using UCB.
next_strategy = select_strategy(stats)

print("\nNext selected strategy:", next_strategy)

print(
    "UCB score:",
    calculate_ucb(next_strategy, stats)
)
