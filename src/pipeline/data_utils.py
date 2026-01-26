import json, os
from pathlib import Path

# Find root folder
def find_project_root():
    current = Path(__file__).parent
    while current != current.parent:
        if current.name == "reddit-nlp":
            return current
        current = current.parent
    return Path(__file__).parent  # Fallback

# Load in stopwords.json
def load_stopwords():
    project_root = find_project_root()
    stopwords_dir = project_root / "src" / "pipeline" / "stopwords.json"
    with open(stopwords_dir, encoding="utf-8") as read_json:
        stopwords = json.load(read_json)
    return set(stopwords) # Return as set for O(1) search

# Load post:comments JSON from latest posts JSON
def load_comments(data_dir):
    project_root = find_project_root()
    comments_dir = project_root / "src" / "data" / data_dir / "post_comments"

    # Get latest time comments were scraped
    latest_comments_time = str(max(comments_dir.glob("./*.json"), key=os.path.getmtime)).split("_")[-1]

    comments_dict = {}

    # List of paths to latest posts
    path_to_comments = comments_dir.glob(f"./*{latest_comments_time}")
    
    # Add post_id as key and list of comments as value to comments_dict
    for p in path_to_comments:
        post_id = p.name
        with open(p, encoding="utf-8") as read_json:
            comments = json.load(read_json)
            comments_dict[post_id] = comments
    
    return comments_dict

def load_analysis(file_name):
    data_dir = find_project_root() / "src" / "data" / "clean"
    with open(f"{data_dir}/{file_name}", encoding="utf-8") as read_json:
        analysis = json.load(read_json)
    return analysis

# Save cleaned comments as JSON
def save_tokens(tokens, file_name):
    project_root = find_project_root()
    clean_dir = project_root / "src" / "data" / "clean" / "post_comments"
    with open(f"{clean_dir}/{file_name}", "w") as json_file:
        json.dump(tokens, json_file, indent=1)

# Save data to JSON
def save_data(data, file_name, data_dir):
    with open(f"{data_dir}/{file_name}", "w") as json_file:
        json.dump(data, json_file, indent=1)
