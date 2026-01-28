import time, praw
import data_utils as ut
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Input: dict of parameters
# Output: Save raw .JSON to /data/raw/ and return dict for comment gathering
def get_raw_data(scrape_config):
    # Unpack parameters
    reddit = scrape_config["praw_instance"]
    sub_name = scrape_config["subreddit"]
    listing, listing_args = scrape_config["listing"], scrape_config["listing_args"]
    from_hours, until_hours = scrape_config["from_hours"], scrape_config["until_hours"]
    data_dir = scrape_config["data_dir"]
    current_date, current_time = scrape_config["current_date"], scrape_config["current_time"]

    # Create data folder for subreddit if does not exist
    subreddit_dir = data_dir / sub_name
    subreddit_dir.mkdir(parents=True, exist_ok=True)

    # Points data_dir to subreddit_dir
    data_dir = subreddit_dir

    # Subreddit instance
    sub = reddit.subreddit(sub_name)

    # Extract posts under given listing
    listing_func = getattr(sub, listing)
    submissions = listing_func(**listing_args)

    # Time range for posts
    time_start = current_time - (from_hours*3600) if from_hours else None
    time_end = current_time - (until_hours*3600) if until_hours else None

    # Dictionary for post id, title and time created and dict for submission obj
    data, data_objects = {}, {}

    # Grabs all submissions from time range
    for submission in submissions:
        time_created = submission.created_utc
        # Handle None cases for time filtering
        if time_start is not None and time_created < time_start:
            continue
        if time_end is not None and time_created > time_end:
            continue
        data[submission.id] = {"title": submission.title, "time_created": time_created}
        data_objects[submission.id] = submission

    # Sort data by time created
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1]["time_created"]))

    # Generate file name save data
    file_name = f"{sub_name}_{current_date}_{current_time}.json"
    ut.save_data(sorted_data, file_name, data_dir)

    # Return for comment extraction
    return data_objects, sorted_data

# Input: dict of post_data and dict of parameters for current scrape
# Output: Save individual posts and their comments to JSON
def gather_comments(data_objects, scrape_config):
    sub_name = scrape_config["subreddit"]
    data_dir = scrape_config["data_dir"]
    current_date, current_time = scrape_config["current_date"], scrape_config["current_time"]

    # Create posts_comments folder for subreddit if does not exist
    subreddit_dir = data_dir / sub_name / "post_comments"
    subreddit_dir.mkdir(parents=True, exist_ok=True)

    # Points data_dir to subreddit_dir / post_comments
    data_dir = subreddit_dir

    # Use threads to scrape comments from posts
    with ThreadPoolExecutor(max_workers=10) as executor:
        for submission in data_objects.values():
            executor.submit(get_post_comments, submission, sub_name, data_dir, current_date, current_time)

# Helper function for getting comments from each post
def get_post_comments(submission, sub_name, data_dir, current_date, current_time):
    # Filter for quality
    if (submission.num_comments > 9 and
        submission.score > 5 and
        not submission.stickied):
            submission.comments.replace_more(limit=10)

            # Filter deleted, removed, and whitespace/empty comments
            all_comments = [c.body for c in submission.comments.list() 
            if c.body and c.body not in ['[deleted]', '[removed]'] and c.body.strip()]

            if all_comments: # Generate file name and save
                file_name = f"{submission.id}_{current_date}_{current_time}.json"
                ut.save_data(all_comments, file_name, data_dir)

# Generate meta data for current scrape
def generate_meta_data(post_data, scrape_config):
    # Unpack parameters
    sub_name = scrape_config["subreddit"]
    listing = scrape_config["listing"]
    from_hours, until_hours = scrape_config["from_hours"], scrape_config["until_hours"]
    current_date, current_time = scrape_config["current_date"], scrape_config["current_time"]

    # Meta data for current scrape
    meta_data = {"subreddit": sub_name, "listing": listing, "date": current_date, "time": current_time, "time_range": {"from_hours": from_hours, "until_hours": until_hours}, "post_count": len(post_data), "posts_file": f"{sub_name}_{current_date}_{current_time}.json", "posts_id": list(post_data.keys())}

    return meta_data
