from reinforcement.strategy_selector import initialize_strategy_stats
from reinforcement.policy_manager import update_strategy_stats

stats = initialize_strategy_stats()

print("Initial statistics:")
print(stats)

stats = update_strategy_stats(stats, "S1", 0.8)
stats = update_strategy_stats(stats, "S1", 1.0)
stats = update_strategy_stats(stats, "S2", 0.6)

print("\nUpdated statistics:")
for strategy_id, data in stats.items():
    print(strategy_id, data)