import argparse
from workflow.graph import run_eduagent


def main():
    parser = argparse.ArgumentParser(
        description="EduAgent: Autonomous Educational Content Generator with RL and Self-Improvement Loops"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Introduction to RAG",
        help="Topic for the lesson (default: 'Introduction to RAG')"
    )
    parser.add_argument(
        "--student-level",
        type=str,
        default="12th-grade graduate with limited English vocabulary",
        help="Target student profile and educational background"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Starting EduAgent Content Generation Workflow")
    print(f"Topic:          {args.topic}")
    print(f"Student Level:  {args.student_level}")
    print("=" * 60)

    result = run_eduagent(
        topic=args.topic,
        student_level=args.student_level
    )

    print("\n" + "=" * 60)
    print("FINAL EXECUTION RESULT")
    print("=" * 60)
    print(f"Final Status:   {result.get('final_status')}")
    print(f"Strategy Used:  {result.get('strategy_id')}")
    print(f"Attempts:       {result.get('attempt')}")
    print(f"Reward:         {result.get('reward')}")

    if result.get("final_status") == "APPROVED":
        print("\nLesson approved successfully!")
        print("\n--- Lesson Preview ---\n")
        lesson = result.get("final_lesson", "")
        print(lesson[:1200] + ("..." if len(lesson) > 1200 else ""))
    else:
        print("\nLesson was not approved within the maximum retry attempts.")


if __name__ == "__main__":
    main()

