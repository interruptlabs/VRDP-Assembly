import ast


def generate(data):
    data["correct_answers"]["When 19"] = 0x1001
    data["correct_answers"]["When 89"] = 0
    data["correct_answers"]["When 231"] = 0


def grade(data):
    total_answers = len(data["correct_answers"])
    correct_count = 0
    feedback_messages = []
    
    for answer_name, correct_value in data["correct_answers"].items():
        if answer_name in data["format_errors"]:
            feedback_messages.append(f"{answer_name}: Please check your answer format.")
            continue
        
        if answer_name not in data["submitted_answers"]:
            feedback_messages.append(f"{answer_name}: No answer provided.")
            continue
        
        submitted = data["submitted_answers"][answer_name]
        
        if submitted == correct_value:
            correct_count += 1
            feedback_messages.append(f"{answer_name}: Correct :)")
        else:
            feedback_messages.append(f"{answer_name}: Incorrect :(")
    
    data["feedback"]["consolidated"] = "\n".join(feedback_messages)
    
    data["score"] = correct_count / total_answers if total_answers > 0 else 0 
