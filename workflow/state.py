
from typing import TypedDict, Any


class AgentState(TypedDict):
    # Student and lesson information
    topic: str
    student_level: str
    reference_material: str

    # Reinforcement learning
    strategy_id: str
    reward: float

    # Lesson generation
    lesson: str
    improvement_instructions: str

    # Evaluation
    evaluation: dict[str, Any]
    rejection_log: list[dict[str, Any]]

    # Retry management
    attempt: int
    max_retries: int

    # Final result
    final_status: str
    final_lesson: str

    topic_analysis: dict[str, Any]
    topic_validation: dict[str, Any]
