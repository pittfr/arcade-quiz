import os
import json
import datetime
import statistics

def log_quiz_data(score, total_questions, question_times=None):
    """log quiz data to a file named with the current day"""

    # create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # generate a date for the filename (YYYY-MM-DD)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(logs_dir, f"{today}.json")

    # calculate median time per question if data available
    time_per_question = None
    if question_times and len(question_times) > 0:
        time_per_question = statistics.median(question_times)
    
    # prepare log data for this session
    log_data = {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "score": score,
        "median_time_per_question": round(time_per_question, 3) if time_per_question is not None else None
    }
    
    # check if file already exists for today
    if os.path.exists(log_file):
        # load existing data
        with open(log_file, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {"sessions_count": 0, "sessions": []}
        
        # add new session to existing data
        if isinstance(existing_data, list):
            existing_data = {
                "sessions_count": len(existing_data),
                "sessions": existing_data
            }
        
        if "sessions" not in existing_data:
            existing_data["sessions"] = []
            
        if "sessions_count" not in existing_data:
            existing_data["sessions_count"] = len(existing_data.get("sessions", []))
        
        # add new session and increment count
        existing_data["sessions"].append(log_data)
        existing_data["sessions_count"] += 1
        
        # write updated data back to file
        with open(log_file, "w") as f:
            json.dump(existing_data, f, indent=4)
    else:
        # create new file with first session
        new_data = {
            "sessions_count": 1,
            "sessions": [log_data]
        }
        with open(log_file, "w") as f:
            json.dump(new_data, f, indent=4)
    
    print(f"Quiz data logged to {log_file}")