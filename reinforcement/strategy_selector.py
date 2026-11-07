import math
from reinforcement.strategies import get_all_strategies
from reinforcement.policy_manager import load_strategy_stats

EXPLORATION_CONSTANT = 1.4


def calculate_ucb(strategy_id, stats):
    strategy = stats[strategy_id]
    count = strategy["count"]

    total_plays = sum(item["count"] for item in stats.values())

    if count == 0:
        return float("inf")

    average_reward = strategy["total_reward"] / count

    exploration = EXPLORATION_CONSTANT * math.sqrt(
        math.log(total_plays) / count
    )

    return average_reward + exploration


def select_strategy():
    stats = load_strategy_stats()
    strategies = get_all_strategies()

    for strategy_id in strategies:
        if stats[strategy_id]["count"] == 0:
            return strategy_id

    scores = {
        sid: calculate_ucb(sid, stats)
        for sid in strategies
    }

    return max(scores, key=scores.get)