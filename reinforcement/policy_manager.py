from reinforcement.strategies import get_all_strategies


def update_strategy_stats(stats, strategy_id, reward):
    # Validate strategy
    if strategy_id not in get_all_strategies():
        raise ValueError(f"Unknown strategy: {strategy_id}")

    # Validate reward
    if not 0 <= reward <= 1:
        raise ValueError("Reward must be between 0 and 1")

    # Update statistics
    stats[strategy_id]["count"] += 1
    stats[strategy_id]["total_reward"] += reward

    stats[strategy_id]["average_reward"] = (
        stats[strategy_id]["total_reward"]
        / stats[strategy_id]["count"]
    )

    return stats