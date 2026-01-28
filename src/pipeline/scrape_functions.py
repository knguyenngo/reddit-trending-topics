import time, praw
from pathlib import Path
import data_utils as ut

# Input: dict of parameters
# Default: None, new, 100 posts, last 24 HOURS
# Output: Save raw .JSON to /data/raw/ and return dict for comment gathering
def get_raw_data(scrape_config):
    # Unpack parameters
    reddit = scrape_config["praw_instance"]
    sub_name = scrape_config["subreddit"]
    listing, listing_args = scrape_config["listing"], scrape_config["listing_args"]
    from_hours, until_hours = scrape_config["from_hours"], scrape_config["until_hours"]
    data_dir = scrape_config["data_dir"]
    current_date, current_time = scrape_config["current_date"], scrape_config["current_time"]

    # Subreddit instance
    sub = reddit.subreddit(sub_name)

    # Extract posts under given listing
    listing_func = getattr(sub, listing)
    submissions = listing_func(**listing_args)

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

    # Sort data by time created
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1]["time_created"]))

    # Generate file name save data
    file_name = f"{sub_name}_{current_date}_{current_time}.json"
    ut.save_data(sorted_data, file_name, data_dir)

    # Return for comment extraction
    return sorted_data

# Input: dict of post_data and dict of parameters for current scrape
# Output: Save individual posts and their comments to JSON
def gather_comments(post_data, scrape_config):
    reddit = scrape_config["praw_instance"]
    data_dir = scrape_config["data_dir"] / "post_comments"
    current_date, current_time = scrape_config["current_date"], scrape_config["current_time"]

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

                file_name = f"{post_id}_{current_date}_{current_time}.json"

                # Save JSON
                ut.save_data(all_comments, file_name, data_dir)

def generate_meta_data(post_data, scrape_config):
    # Unpack parameters
    reddit = scrape_config["praw_instance"]
    sub_name = scrape_config["subreddit"]
    listing, listing_args = scrape_config["listing"], scrape_config["listing_args"]
    from_hours, until_hours = scrape_config["from_hours"], scrape_config["until_hours"]
    data_dir = scrape_config["data_dir"]
    current_date, current_time = scrape_config["current_date"], scrape_config["current_time"]

    # Meta data for current scrape
    meta_data = {"subreddit": sub_name, "date": current_date, "time": current_time, "time_range": {"from_hours": from_hours, "until_hours": until_hours}, "post_count": len(post_data), "posts_file": f"{sub_name}_{current_date}_{current_time}.json", "posts_id": list(post_data.keys())}

    return meta_data
