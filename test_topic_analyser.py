from pathlib import Path
from agents.topic_analyzer import analyze_topic

reference = Path(
    "knowledge/rag_reference.md"
).read_text(encoding="utf-8")

result = analyze_topic(
    topic="Introduction to RAG",
    student_level="12th-grade graduate with limited English vocabulary",
    reference_material=reference
)

print("\nTOPIC ANALYSIS")
print("Definition:", result["correct_definition"])

print("\nEssential Concepts:")
for item in result["essential_concepts"]:
    print("-", item)

print("\nCommon Misunderstandings:")
for item in result["common_misunderstandings"]:
    print("-", item)