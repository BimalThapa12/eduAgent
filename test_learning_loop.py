
from reinforcement.strategy_selector import select_strategy
from reinforcement.policy_manager import update_strategy_stats

# Select strategy
selected = select_strategy()
print("Selected strategy:", selected)

# Simulate evaluator reward
reward = 0.85

# Save reward in SQLite
update_strategy_stats(selected, reward)
print("Reward saved:", reward)

# Select next strategy
next_selected = select_strategy()
print("Next selected strategy:", next_selected)