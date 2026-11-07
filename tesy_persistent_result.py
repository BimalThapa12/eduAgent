
from reinforcement.policy_manager import (
    load_strategy_stats,
    update_strategy_stats
)

print("Before update:")
print(load_strategy_stats())

print("\nSaving reward...")

update_strategy_stats("S1", 0.8)
update_strategy_stats("S1", 1.0)

print("\nAfter update:")
print(load_strategy_stats())