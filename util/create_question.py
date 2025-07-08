import os
import json
import uuid
from pathlib import Path
import shutil


def create_question(module, assessment, zone, question, title, question_type):
    assessment_file = Path("course/courseInstances/base/assessments") / module / assessment / "infoAssessment.json"
    if not assessment_file.exists():
        print(f"Error: Assessment '{module}/{assessment}' not found")
        print(f"Expected file: {assessment_file}")
        print("Create the assessment first using: python3 -m util create_assessment")
        return
    
    question_dir = Path("course/questions") / module / assessment / zone / question
    question_dir.mkdir(parents=True, exist_ok=True)
    
    question_uuid = str(uuid.uuid4())
    
    with open(assessment_file, "r") as f:
        assessment_data = json.load(f)
    topic = f"{assessment_data['module']} - {assessment_data['title']}"
    
    template_dir = Path("util/templates") / question_type
    if not template_dir.exists():
        print(f"Error: Template '{question_type}' not found in util/templates/")
        print("Available templates:")
        templates_dir = Path("util/templates")
        if templates_dir.exists():
            for template in templates_dir.iterdir():
                if template.is_dir():
                    print(f"  - {template.name}")
        else:
            print("  No templates found")
        return

    info_template = template_dir / "info.json"
    info_content = info_template.read_text()
    info_content = info_content.replace("{uuid}", question_uuid)
    info_content = info_content.replace("{title}", title)
    info_content = info_content.replace("{topic}", topic)
    
    with open(question_dir / "info.json", "w") as f:
        f.write(info_content)
    
    html_template = template_dir / "question.html"
    html_content = html_template.read_text()
    
    with open(question_dir / "question.html", "w") as f:
        f.write(html_content)
    
    for python_file in template_dir.glob("*.py"):
        if python_file.name == "server.py":
            shutil.copy(python_file, question_dir / "server.py")
        else:
            tests_dir = question_dir / "tests"
            tests_dir.mkdir(exist_ok=True)
            shutil.copy(python_file, tests_dir / python_file.name)
    
    question_id = f"{module}/{assessment}/{zone}/{question}"
    
    zone_found = False
    
    for assessment_zone in assessment_data.get("zones", []):
        if assessment_zone.get("title", "").lower() == zone.lower():
            assessment_zone["questions"].append({"id": question_id, "points": 1})
            zone_found = True
            break
    
    if not zone_found:
        print(f"Error: Zone '{zone}' not found in assessment '{module}/{assessment}'")
        print("Available zones:")
        for assessment_zone in assessment_data.get("zones", []):
            print(f"  - {assessment_zone.get('title', 'Unknown').lower()}")
        return
    
    with open(assessment_file, "w") as f:
        json.dump(assessment_data, f, indent=4)
        f.write("\n")
