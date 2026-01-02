import json, time, sys, praw, getopt, os
from pathlib import Path
import os

options = "i:"
long_options = ["input="]
ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_CLIENT_SECRET")
AGENT = os.getenv("REDDIT_USER_AGENT", "topic-modeler")

# Find root folder
def find_project_root():
    current = Path(__file__).parent
    while current != current.parent:
        if current.name == "Reddit_Scraper":
            return current
        current = current.parent
    return Path(__file__).parent  # Fallback

project_root = find_project_root()
data_dir = project_root / "src" / "data" / "raw" / "post_comments"

def gather_comments(path):
    # Load posts JSON: id, title, time created
    try:
        with open(path, "r") as posts:
            post_data = json.load(posts)
    # No file for given path
    except FileNotFoundError:
        print(f"File not found: {path}")
        return
    # Decoding error
    except json.decoder.JSONDecodeError as e:
        print(f"JSON decode error in file: {path}")
        print(f"Error: {e}")
        return

    # Reddit instance
    reddit = praw.Reddit(
        client_id=ID,
        client_secret=SECRET,
        user_agent=AGENT
    )

    # Current date and time of data extraction
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    current_time = time.time()

    # Gather comments from post ID
    for post_id in post_data.keys():
        submission = reddit.submission(id=post_id)

        # Filter for quality
        if (submission.num_comments > 9 and
            submission.score > 5 and
            not submission.stickied):
                submission.comments.replace_more(limit=None)

                # Filter deleted, removed, and whitespace/empty comments
                all_comments = [c.body for c in submission.comments.list() 
                if c.body and c.body not in ['[deleted]', '[removed]'] and c.body.strip()]

                filename = data_dir / f"{post_id}_{current_date}_{current_time}.json"

                # Save JSON
                with open(filename, "w") as json_file:
                    json.dump(all_comments, json_file, indent=1)

def main():
    args = sys.argv[1:]
    file_path = ""

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-i", "--input"):
                file_path = currentVal
    except getopt.error as err:
        print(str(err))
 
    gather_comments(file_path)

if __name__ == "__main__":
    main()
