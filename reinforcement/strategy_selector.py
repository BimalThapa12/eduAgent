
import math

from reinforcement.strategies import get_all_strategies


# Exploration parameter
EXPLORATION_CONSTANT = 1.4


def initialize_strategy_stats():

    strategies = get_all_strategies()

    stats = {}

    for strategy_id in strategies:

        stats[strategy_id] = {
            "count": 0,
            "total_reward": 0.0,
            "average_reward": 0.0
        }

    return stats


def calculate_ucb(strategy_id, stats):

    strategy = stats[strategy_id]

    count = strategy["count"]

    total_plays = sum(
        item["count"]
        for item in stats.values()
    )

    # Unselected strategies receive priority.
    if count == 0:
        return float("inf")

    average_reward = (
        strategy["total_reward"] / count
    )

    exploration = EXPLORATION_CONSTANT * math.sqrt(
        math.log(total_plays) / count
    )

    ucb_score = average_reward + exploration

    return ucb_score


def select_strategy(stats):

    strategies = get_all_strategies()

    # First, explore every strategy at least once.
    for strategy_id in strategies:

        if stats[strategy_id]["count"] == 0:

            return strategy_id

    # Calculate UCB scores.
    scores = {}

    for strategy_id in strategies:

        scores[strategy_id] = calculate_ucb(
            strategy_id,
            stats
        )

    # Select the strategy with the highest UCB score.
    selected_strategy = max(
        scores,
        key=scores.get
    )

    return selected_strategy
