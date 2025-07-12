import os
import json
import uuid
from pathlib import Path


def create_assessment(module, assessment, title, number):
    assessment_dir = Path("course/courseInstances/base/assessments") / module / assessment
    
    assessment_dir.mkdir(parents=True, exist_ok=True)
    
    assessment_uuid = str(uuid.uuid4())

    number_code = {
        "arm64": "A64",
        "arm32": "A32",
        "x64": "X64",
    }[module]
    
    assessment_info = {
        "uuid": assessment_uuid,
        "type": "Homework",
        "title": f"{module.upper()} - {title}",
        "set": "Quiz",
        "module": module.upper(),
        "number": f"{number_code}-{number}",
        "allowAccess": [
            {
                "active": True
            }
        ],
        "zones": [
            {
                "title": "Regular",
                "advanceScorePerc": 100,
                "questions": []
            },
            {
                "title": "Bonus",
                "questions": []
            }
        ]
    }

    info_file = assessment_dir / "infoAssessment.json"
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(assessment_info, f, indent=4, ensure_ascii=False)
        f.write("\n")  # Ensure newline at end of file
