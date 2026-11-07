
import json
from pathlib import Path
from datetime import datetime

from langgraph.graph import StateGraph, START, END

from workflow.state import AgentState

from agents.topic_analyzer import analyze_topic
from agents.topic_validator import validate_topic_alignment
from agents.generator import generate_lesson, regenerate_lesson
from agents.evaluator import evaluate_lesson
from agents.improvement_agent import create_improvement_instructions

from reinforcement.strategy_selector import select_strategy
from reinforcement.reward import calculate_reward
from reinforcement.policy_manager import update_strategy_stats

from utils.logger import (
    print_header,
    print_step,
    print_success,
    print_warning,
    print_error,
    print_evaluation,
    print_final_summary,
    get_log_file
)


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

REFERENCE_FILE = BASE_DIR / "knowledge" / "rag_reference.md"
LESSON_DIR = BASE_DIR / "outputs" / "lessons"
LOG_DIR = BASE_DIR / "outputs" / "evaluation_logs"


# --------------------------------------------------
# LOAD REFERENCE MATERIAL
# --------------------------------------------------

def load_reference_material():

    if not REFERENCE_FILE.exists():
        raise FileNotFoundError(
            f"Reference file not found: {REFERENCE_FILE}"
        )

    material = REFERENCE_FILE.read_text(encoding="utf-8")

    if not material.strip():
        raise ValueError("Reference material is empty.")

    return material


# --------------------------------------------------
# NODE 1: SELECT GENERATION STRATEGY
# --------------------------------------------------

def select_generation_strategy(state: AgentState):

    print_step("Selecting generation strategy...")

    strategy_id = select_strategy()

    print_success(
        f"Generation strategy selected: {strategy_id}"
    )

    return {
        "strategy_id": strategy_id,
        "attempt": 0,
        "rejection_log": []
    }


# --------------------------------------------------
# NODE 2: ANALYZE TOPIC REQUIREMENTS
# --------------------------------------------------

def analyze_topic_requirements(state: AgentState):

    print_step("Analyzing RAG topic requirements...")

    analysis = analyze_topic(
        topic=state["topic"],
        student_level=state["student_level"],
        reference_material=state["reference_material"]
    )

    print_success("Topic analysis completed.")

    print_step("Essential learning concepts:")

    for index, concept in enumerate(
        analysis["essential_concepts"], start=1
    ):
        print_step(f"{index}. {concept}")

    return {
        "topic_analysis": analysis
    }


# --------------------------------------------------
# NODE 3: GENERATE OR REGENERATE LESSON
# --------------------------------------------------

def generate(state: AgentState):

    attempt = state["attempt"]

    print_header(
        f"LESSON GENERATION - ATTEMPT {attempt + 1}"
    )

    if attempt == 0:

        lesson = generate_lesson(
            topic=state["topic"],
            strategy_id=state["strategy_id"],
            student_level=state["student_level"],
            reference_material=state["reference_material"],
            topic_analysis=state["topic_analysis"]
        )

    else:

        lesson = regenerate_lesson(
            topic=state["topic"],
            strategy_id=state["strategy_id"],
            student_level=state["student_level"],
            previous_lesson=state["lesson"],
            improvement_instructions=state["improvement_instructions"],
            reference_material=state["reference_material"],
            topic_analysis=state["topic_analysis"]
        )

    if not lesson or not lesson.strip():
        raise ValueError(
            "Lesson generation returned empty content."
        )

    print_success("Lesson generated successfully.")

    return {
        "lesson": lesson,
        "attempt": attempt + 1
    }


# --------------------------------------------------
# NODE 4: EVALUATE LESSON
# --------------------------------------------------

def evaluate(state: AgentState):

    print_step("Validating topic alignment...")

    topic_result = validate_topic_alignment(
        topic_analysis=state["topic_analysis"],
        lesson=state["lesson"]
    )

    if topic_result["valid"]:

        print_success(
            f"Topic validation passed. Coverage: "
            f"{topic_result.get('coverage', 'N/A')}"
        )

    else:

        print_error(
            f"Topic validation failed: {topic_result['reason']}"
        )

    print_step("Evaluating lesson against R1-R8...")

    evaluation = evaluate_lesson(
        topic=state["topic"],
        lesson=state["lesson"],
        reference_material=state["reference_material"]
    )

    # Verify all eight evaluation checkpoints.
    expected_ids = {f"R{i}" for i in range(1, 9)}

    checks = evaluation.get("checks", [])

    actual_ids = {
        check.get("id")
        for check in checks
    }

    if (
        len(checks) != 8
        or actual_ids != expected_ids
        or any(
            check.get("status") not in ("PASS", "FAIL")
            for check in checks
        )
    ):
        raise ValueError(
            "Evaluator returned an invalid R1-R8 result."
        )

    # Independent topic validation gate.
    if not topic_result["valid"]:

        evaluation["checks"] = [
            {
                **check,
                "status": "FAIL",
                "feedback": topic_result["reason"]
            }
            if check["id"] == "R1" else check
            for check in evaluation["checks"]
        ]

    # Calculate approval locally.
    evaluation["approved"] = (
        topic_result["valid"]
        and all(
            check["status"] == "PASS"
            for check in evaluation["checks"]
        )
    )

    # Write readable evaluation to logs.
    print_evaluation(evaluation)

    rejection_log = list(state["rejection_log"])

    if not evaluation["approved"]:

        rejection_log.append({
            "attempt": state["attempt"],
            "topic_validation": topic_result,
            "checks": evaluation["checks"]
        })

    return {
        "evaluation": evaluation,
        "topic_validation": topic_result,
        "rejection_log": rejection_log
    }


# --------------------------------------------------
# NODE 5: CREATE IMPROVEMENT INSTRUCTIONS
# --------------------------------------------------

def create_improvements(state: AgentState):

    print_warning(
        "Lesson failed evaluation. Preparing improvements..."
    )

    instructions = create_improvement_instructions(
        state["evaluation"]
    )

    if not state["topic_validation"]["valid"]:

        instructions += (
            "\n\nTOPIC VALIDATION FAILURE:\n"
            + state["topic_validation"]["reason"]
            + "\nCorrect the lesson so it accurately explains "
              "Retrieval-Augmented Generation (RAG)."
        )

    print_success("Improvement instructions created.")

    return {
        "improvement_instructions": instructions
    }


# --------------------------------------------------
# ROUTE AFTER EVALUATION
# --------------------------------------------------

def route_after_evaluation(state: AgentState):

    if state["evaluation"]["approved"]:
        return "approve"

    if state["attempt"] <= state["max_retries"]:
        return "improve"

    return "reject"


# --------------------------------------------------
# FINAL REWARD CALCULATION
# --------------------------------------------------

def get_final_reward(state: AgentState):

    reward = calculate_reward(state["evaluation"])

    if not state["topic_validation"]["valid"]:
        reward = min(reward, 0.5)

    return reward


# --------------------------------------------------
# NODE 6: APPROVE LESSON
# --------------------------------------------------

def approve_lesson(state: AgentState):

    if not state["evaluation"]["approved"]:
        raise ValueError(
            "Cannot approve a failed lesson."
        )

    if not state["topic_validation"]["valid"]:
        raise ValueError(
            "Cannot approve a lesson that failed topic validation."
        )

    reward = get_final_reward(state)

    update_strategy_stats(
        state["strategy_id"],
        reward
    )

    print_success("Lesson approved successfully.")

    return {
        "reward": reward,
        "final_status": "APPROVED",
        "final_lesson": state["lesson"]
    }


# --------------------------------------------------
# NODE 7: REJECT LESSON
# --------------------------------------------------

def reject_lesson(state: AgentState):

    reward = get_final_reward(state)

    update_strategy_stats(
        state["strategy_id"],
        reward
    )

    print_error(
        "Lesson rejected after maximum regeneration attempts."
    )

    return {
        "reward": reward,
        "final_status": "REJECTED",
        "final_lesson": ""
    }


# --------------------------------------------------
# NODE 8: SAVE OUTPUTS
# --------------------------------------------------

def save_outputs(state: AgentState):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    LESSON_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Save approved lessons only.
    if state["final_status"] == "APPROVED":

        lesson_path = (
            LESSON_DIR / f"lesson_{timestamp}.md"
        )

        lesson_path.write_text(
            state["final_lesson"],
            encoding="utf-8"
        )

        print_success(
            f"Approved lesson saved: {lesson_path}"
        )

    # Save structured JSON evaluation history.
    log_path = (
        LOG_DIR / f"evaluation_{timestamp}.json"
    )

    log_data = {
        "topic": state["topic"],
        "strategy_id": state["strategy_id"],
        "attempts": state["attempt"],
        "final_status": state["final_status"],
        "reward": state["reward"],
        "topic_analysis": state["topic_analysis"],
        "topic_validation": state["topic_validation"],
        "rejection_log": state["rejection_log"],
        "final_evaluation": state["evaluation"]
    }

    log_path.write_text(
        json.dumps(log_data, indent=4),
        encoding="utf-8"
    )

    print_success(
        f"Evaluation JSON saved: {log_path}"
    )

    # Write readable final summary.
    print_final_summary(state)

    print_success(
        f"Readable workflow log saved: {get_log_file()}"
    )

    return {}


# --------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# --------------------------------------------------

def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node(
        "select_strategy",
        select_generation_strategy
    )

    builder.add_node(
        "analyze_topic",
        analyze_topic_requirements
    )

    builder.add_node(
        "generate",
        generate
    )

    builder.add_node(
        "evaluate",
        evaluate
    )

    builder.add_node(
        "improve",
        create_improvements
    )

    builder.add_node(
        "approve",
        approve_lesson
    )

    builder.add_node(
        "reject",
        reject_lesson
    )

    builder.add_node(
        "save",
        save_outputs
    )

    # Workflow connections.
    builder.add_edge(START, "select_strategy")

    builder.add_edge(
        "select_strategy",
        "analyze_topic"
    )

    builder.add_edge(
        "analyze_topic",
        "generate"
    )

    builder.add_edge(
        "generate",
        "evaluate"
    )

    # Conditional evaluation routing.
    builder.add_conditional_edges(
        "evaluate",
        route_after_evaluation,
        {
            "approve": "approve",
            "improve": "improve",
            "reject": "reject"
        }
    )

    # Regeneration loop.
    builder.add_edge(
        "improve",
        "generate"
    )

    # Final workflow connections.
    builder.add_edge("approve", "save")
    builder.add_edge("reject", "save")

    builder.add_edge("save", END)

    return builder.compile()


# Compile the graph.
eduagent_graph = build_graph()


# --------------------------------------------------
# MAIN EXECUTION FUNCTION
# --------------------------------------------------

def run_eduagent(
    topic: str,
    student_level: str
):

    print_header("EDUAGENT AI - CONTENT GENERATION WORKFLOW")

    print_step(f"Topic: {topic}")
    print_step(f"Student Level: {student_level}")

    initial_state = {
        "topic": topic,
        "student_level": student_level,

        "reference_material": load_reference_material(),

        "strategy_id": "",
        "reward": 0.0,

        "lesson": "",
        "improvement_instructions": "",

        "evaluation": {},
        "rejection_log": [],

        "attempt": 0,
        "max_retries": 2,

        "final_status": "",
        "final_lesson": "",

        "topic_analysis": {},
        "topic_validation": {}
    }

    return eduagent_graph.invoke(initial_state)
