import json, time, sys, praw, getopt
from pathlib import Path

options = "s:nhtcl:f:u:"
long_options = ["subreddit=", "new", "hot", "controversial", "top", "limit=", "from-hours=", "until-hours="]
ID = "REDACTED_ID"
SECRET = "REDACTED_SECRET"
AGENT = "topic-modeler"

# Find root folder
def find_project_root():
    current = Path(__file__).parent
    while current != current.parent:
        if current.name == "Reddit_Scraper":
            return current
        current = current.parent
    return Path(__file__).parent  # Fallback

project_root = find_project_root()
data_dir = project_root / "src" / "data" / "raw"

# Input: Sub name, listing, post limit, time range
# Default: None, new, 100 posts, last 24 HOURS
# Output: Save raw .JSON to /data/raw/
def get_raw_data(sub_name, from_hours, until_hours, listing="new", listing_args={"limit":100}):
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

def main():
    # Read in arguments
    args = sys.argv[1:]
    sub_name = ""
    listing = ""
    listing_args = None
    time_range = None

    # Parse options and values
    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-s", "--subreddit"):
                sub_name = currentVal
            elif currentArg in ("-n", "--new"):
                listing = "new"
            elif currentArg in ("-h", "--hot"):
                listing = "hot"
            elif currentArg in ("-t", "--top"):
                listing = "top"
            elif currentArg in ("-c", "--controversial"):
                listing = "controversial"
            elif currentArg in ("-l", "--limit"):
                listing_args = {"limit": int(currentVal)}
            elif currentArg in ("-f", "--from-hours"):
                from_hours = int(currentVal)
            elif currentArg in ("-u", "--until-hours"):
                until_hours = int(currentVal)
    except getopt.error as err:
        print(str(err))

    # Scrape all posts under listing within time range
    get_raw_data(sub_name, from_hours, until_hours, listing, listing_args)

if __name__ == "__main__":
    main()
