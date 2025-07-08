import os
import json
import uuid
from pathlib import Path


def create_assessment(module, assessment, title, number):
    """
    Create a new assessment with the specified parameters.
    
    Args:
        module: Module name (e.g., "arm64")
        assessment: Assessment name (e.g., "basics_1")
        title: Assessment title (e.g., "Basics 1")
        number: Assessment number (e.g., "B1")
    """
    
    assessment_dir = Path("course/courseInstances/base/assessments") / module / assessment
    
    assessment_dir.mkdir(parents=True, exist_ok=True)
    
    assessment_uuid = str(uuid.uuid4())
    
    assessment_info = {
        "uuid": assessment_uuid,
        "type": "Homework",
        "title": title,
        "set": "Quiz",
        "module": module.upper(),
        "number": f"{module.upper()}-{number}",
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
