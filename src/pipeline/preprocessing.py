import re, string, json, unicodedata, os
from pathlib import Path
import scrape_functions as sf

# Clean comments
def clean(text):
    text = unicodedata.normalize("NFKD", text) # Normalize text
    text= text.lower() # Lowercase text
    text = re.sub(r"\d+", "", text) # Remove numbers
    text = re.sub(r"http\S+", "", text) # Remove links
    text = re.sub(r"[\u2019]|'", "#'#", text) # Replace middle apostrophe with pattern to save
    text = re.sub(r"(?!#)\W(?!#)|(?!')#|#(?!')", " ", text) # Remove all special chars
    text = re.sub(r"#'#", "'", text) # Revert middle apostrophe back
    return text

# Tokenize into unigrams
def tokenize(text):
    tokens = text.split()
    return tokens

# Remove stopwords from list of tokens
def remove_stopwords(tokens, stopwords):
    tokens = [t for t in tokens if t not in stopwords] # Remove stopwords
    return tokens

# Load in stopwords.json
def load_stopwords():
    with open("./stopwords.json", mode="r", encoding="utf-8") as read_json:
        stopwords = json.load(read_json)
    return set(stopwords) # Return as set for O(1) search

# Clean and tokenize text
def preprocess_comment(text, stopwords):
    text = clean(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens, stopwords)
    return tokens

# Load post:comments JSON from latest posts JSON
def load_comments(dir):
    project_root = sf.find_project_root()
    comments_dir = project_root / "src" / "data" / dir / "post_comments"

    # Get latest time comments were scraped
    latest_comments_time = str(max(comments_dir.glob("./*.json"), key=os.path.getmtime)).split("_")[-1]

    comments_dict = {}

    # List of paths to latest posts
    path_to_comments = comments_dir.glob(f"./*{latest_comments_time}")
    
    # Add post_id as key and list of comments as value to comments_dict
    for p in path_to_comments:
        post_id = p.name
        with open(p, mode="r", encoding="utf-8") as read_json:
            comments = json.load(read_json)
            comments_dict[post_id] = comments
    
    return comments_dict

# Save cleaned comments as JSON
def save_tokens(tokens, file_name):
    project_root = sf.find_project_root()
    clean_dir = project_root / "src" / "data" / "clean" / "post_comments"
    with open(f"{clean_dir}/{file_name}", "w") as json_file:
        json.dump(tokens, json_file, indent=1)
