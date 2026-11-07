from reinforcement.strategies import get_all_strategies
from memory.database import get_connection


def load_strategy_stats():
    stats = {}

    for strategy_id in get_all_strategies():
        stats[strategy_id] = {
            "count": 0,
            "total_reward": 0.0,
            "average_reward": 0.0
        }

    connection = get_connection()
    cursor = connection.cursor()

    rows = cursor.execute(
        "SELECT * FROM strategy_stats"
    ).fetchall()

    for row in rows:
        stats[row["strategy_id"]] = {
            "count": row["count"],
            "total_reward": row["total_reward"],
            "average_reward": row["average_reward"]
        }

    connection.close()
    return stats


def update_strategy_stats(strategy_id, reward):
    if strategy_id not in get_all_strategies():
        raise ValueError(f"Unknown strategy: {strategy_id}")

    if not 0 <= reward <= 1:
        raise ValueError("Reward must be between 0 and 1")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO strategy_stats
        (strategy_id, count, total_reward, average_reward)
        VALUES (?, 1, ?, ?)

        ON CONFLICT(strategy_id) DO UPDATE SET
            count = count + 1,
            total_reward = total_reward + excluded.total_reward,
            average_reward =
                (total_reward + excluded.total_reward) / (count + 1)
    """, (strategy_id, reward, reward))

    connection.commit()
    connection.close()

    return load_strategy_stats()