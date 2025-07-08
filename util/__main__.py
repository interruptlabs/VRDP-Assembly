import sys
import argparse
from . import create_assessment, create_question


def main():
    parser = argparse.ArgumentParser(description="PrairieLearn utility commands")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create assessment command
    create_assessment_parser = subparsers.add_parser("create_assessment", 
                                                   help="Create a new assessment")
    create_assessment_parser.add_argument("--module", required=True, 
                                        help="Module name (e.g., arm64)")
    create_assessment_parser.add_argument("--assessment", required=True, 
                                        help="Assessment name (e.g., basics_1)")
    create_assessment_parser.add_argument("--title", required=True, 
                                        help="Assessment title (e.g., \"Basics 1\")")
    create_assessment_parser.add_argument("--number", required=True, 
                                        help="Assessment number (e.g., \"B1\")")
    
    # Create question command
    create_question_parser = subparsers.add_parser("create_question",
                                                 help="Create a new question")
    create_question_parser.add_argument("--module", required=True,
                                      help="Module name (e.g., arm64)")
    create_question_parser.add_argument("--assessment", required=True,
                                      help="Assessment name (e.g., basics_1)")
    create_question_parser.add_argument("--zone", required=True,
                                      choices=["regular", "bonus"],
                                      help="Zone (regular or bonus)")
    create_question_parser.add_argument("--question", required=True,
                                      help="Question name (e.g., add)")
    create_question_parser.add_argument("--title", required=True,
                                      help="Question title")
    create_question_parser.add_argument("--type", required=True,
                                      help="Question type (e.g., arm64_write)")
    
    args = parser.parse_args()
    
    if args.command == "create_assessment":
        create_assessment.create_assessment(
            module=args.module,
            assessment=args.assessment,
            title=args.title,
            number=args.number
        )
    elif args.command == "create_question":
        create_question.create_question(
            module=args.module,
            assessment=args.assessment,
            zone=args.zone,
            question=args.question,
            title=args.title,
            question_type=args.type
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
