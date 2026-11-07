
from workflow.graph import run_eduagent

result = run_eduagent(
    topic="Introduction to RAG",
    student_level="12th-grade graduate with limited English vocabulary"
)

print("\n========== FINAL RESULT ==========")
print("Status:", result["final_status"])
print("Strategy:", result["strategy_id"])
print("Attempts:", result["attempt"])
print("Reward:", result["reward"])

if result["final_status"] == "APPROVED":
    print("\nLesson approved successfully!")
    print(result["final_lesson"][:1500])
else:
    print("\nLesson rejected after maximum attempts.")
