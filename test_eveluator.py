
from agents.evaluator import validate_evaluation_evidence


test_checks = [
    {
        "id": "R1",
        "status": "PASS",
        "evidence": "Explanation of the decision",
        "feedback": ""
    },
    {
        "id": "R2",
        "status": "PASS",
        "evidence": "The lesson explains retrieval using external documents.",
        "feedback": ""
    }
]


result = validate_evaluation_evidence(test_checks)

for check in result:

    print(
        check["id"],
        check["status"],
        check["evidence"],
        check["feedback"]
    )
