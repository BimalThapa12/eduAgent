
from pathlib import Path
from datetime import datetime
import sys
import time

# --------------------------------------------------
# LOG DIRECTORY AND FILE
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"workflow_{TIMESTAMP}.txt"


# --------------------------------------------------
# FILE LOGGING
# --------------------------------------------------

def write_log(message=""):
    """Save messages to the workflow log file."""

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(str(message) + "\n")
        file.flush()


# --------------------------------------------------
# INSTANT TERMINAL LOGGING
# --------------------------------------------------

def live_log(message="", level="INFO"):
    """Display messages immediately and save them."""

    formatted = f"[{level}] {message}"

    print(formatted, flush=True)
    write_log(formatted)


# --------------------------------------------------
# OPTIONAL TYPING EFFECT
# Used only for Ollama-generated content.
# --------------------------------------------------

def type_log(message="", level="INFO", delay=0.015):
    """Display text character by character."""

    formatted = f"[{level}] {message}"

    for character in formatted:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)

    sys.stdout.write("\n")
    sys.stdout.flush()

    write_log(formatted)


# --------------------------------------------------
# WORKFLOW MESSAGES
# --------------------------------------------------

def print_header(title):
    line = "=" * 65

    live_log(line)
    live_log(title.center(65))
    live_log(line)


def print_step(message):
    live_log(message, "INFO")


def print_success(message):
    live_log(message, "SUCCESS")


def print_warning(message):
    live_log(message, "WARNING")


def print_error(message):
    live_log(message, "ERROR")


# --------------------------------------------------
# EVALUATION LOGGING
# --------------------------------------------------

def print_evaluation(evaluation):

    print_header("LESSON QUALITY EVALUATION")

    checks = evaluation.get("checks", [])

    for check in checks:

        status = check.get("status", "UNKNOWN")

        level = "SUCCESS" if status == "PASS" else "ERROR"

        live_log(
            f"{check.get('id')} - "
            f"{check.get('name')} : {status}",
            level
        )

        write_log(
            f"Evidence: {check.get('evidence', 'Not provided')}"
        )

        feedback = check.get("feedback", "")

        if feedback:
            write_log(f"Feedback: {feedback}")

    live_log("-" * 65)

    live_log("OVERALL EVALUATION FEEDBACK")

    live_log(
        evaluation.get(
            "overall_feedback",
            "No overall feedback provided."
        )
    )

    if evaluation.get("approved"):
        print_success("Lesson evaluation: APPROVED")
    else:
        print_error("Lesson evaluation: REJECTED")


# --------------------------------------------------
# FINAL EXECUTION SUMMARY
# --------------------------------------------------

def print_final_summary(state):

    print_header("FINAL EXECUTION SUMMARY")

    live_log(f"Topic             : {state.get('topic', 'N/A')}")
    live_log(f"Student Level     : {state.get('student_level', 'N/A')}")
    live_log(f"Strategy          : {state.get('strategy_id', 'N/A')}")
    live_log(f"Attempts          : {state.get('attempt', 'N/A')}")
    live_log(f"Final Status      : {state.get('final_status', 'N/A')}")
    live_log(f"Reward            : {state.get('reward', 'N/A')}")

    validation = state.get("topic_validation", {})

    live_log("")
    live_log("TOPIC VALIDATION")

    live_log(
        f"Status            : "
        f"{'PASS' if validation.get('valid') else 'FAIL'}"
    )

    live_log(
        f"Concept Coverage  : "
        f"{validation.get('coverage', 'N/A')}"
    )

    live_log("=" * 65)

    live_log(
        f"Workflow log saved at: {LOG_FILE}",
        "SUCCESS"
    )


# --------------------------------------------------
# GET LOG FILE PATH
# --------------------------------------------------

def get_log_file():
    return LOG_FILE
