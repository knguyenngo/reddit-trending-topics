import os
import json, time, praw
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_CLIENT_SECRET")
AGENT = os.getenv("REDDIT_USER_AGENT", "topic-modeler")

# Find root folder
def find_project_root():
    current = Path(__file__).parent
    while current != current.parent:
        if current.name == "reddit-nlp":
            return current
        current = current.parent
    return Path(__file__).parent  # Fallback

# Input: Sub name, listing, post limit, time range
# Default: None, new, 100 posts, last 24 HOURS
# Output: Save raw .JSON to /data/raw/
def get_raw_data(sub_name, from_hours, until_hours, listing="new", listing_args={"limit":100}):
    # Save to this dir
    project_root = find_project_root()
    data_dir = project_root / "src" / "data" / "raw"

    # Reddit instance
    reddit = praw.Reddit(
        client_id=ID,
        client_secret=SECRET,
        user_agent=AGENT
    )

    # Subreddit instance
    sub = reddit.subreddit(sub_name)

    # Extract posts under given listing
    listing_func = getattr(sub, listing)
    submissions = listing_func(**listing_args)

    # Current date and time of data extraction
    current_date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    current_time = time.time()

    # Time range for posts
    time_start = time.time() - (from_hours*3600) if from_hours else None
    time_end = time.time() - (until_hours*3600) if until_hours else None
    
    # Dictionary for post id, title and time created
    data = {}

    # Grabs all submissions from time range
    for submission in submissions:
        time_created = submission.created_utc

        if (time_created >= time_start and time_created <= time_end):
            data[submission.id] = {"title": submission.title, "time_created": time_created}

    sorted_data = dict(sorted(data.items(), key=lambda x: x[1]["time_created"]))
    # JSON filename
    filename = data_dir / f"posts_{current_date}_{current_time}.json"
    # Save JSON
    with open(filename, "w") as json_file:
        json.dump(sorted_data, json_file, indent=1)
    print(filename)

# Input: path to POST.JSON
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

    # Save comments.JSON to this dir
    project_root = find_project_root()
    data_dir = project_root / "src" / "data" / "raw" / "post_comments"

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

