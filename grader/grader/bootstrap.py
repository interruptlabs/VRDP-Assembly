import json
from pathlib import Path
from traceback import format_exception

from grader import AssemblyError


def main():
    results_directory_path = Path("/grade/results")
    results_directory_path.mkdir(exist_ok=True, parents=True)
    results_file_path = results_directory_path / "results.json"

    try:
        answer_file_path = Path("/grade/student/answer.s")
        answer = answer_file_path.read_text()

        from grader.grader import Grader

        correct, outputs = Grader.grade(answer)

        tests = []
        for name, output in outputs:
            tests.append({
                "name": name,
                "points": 0,
                "max_points": 0,
                "output": output
            })

        results_file_path.write_text(json.dumps({
            "gradable": True,
            "score": 1 if correct else 0,
            "tests": tests
        }))
        
    except AssemblyError as e:
        results_file_path.write_text(json.dumps({
            "gradable": True,
            "score": 0,
            "output": str(e)
        }))

    except Exception as e:
        results_file_path.write_text(json.dumps({
            "gradable": True,
            "score": 0,
            "output": "".join(format_exception(e))
        }))


if __name__ == "__main__":
    main()
