import json, time, sys, praw, getopt

options = "s:nhtcl:dwm"
long_options = ["subreddit=", "new", "hot", "controversial", "top", "limit=", "day", "week", "month"]
ID = "REDACTED_ID"
SECRET = "REDACTED_SECRET"
AGENT = "topic-modeler"

# Input: Sub name, listing, post limit, time range
# Default: None, new, 100 posts, last 24 HOURS
# Output: Save raw .JSON to /data/raw/
def get_raw_data(sub_name, listing="new", listing_args={"limit":100}, time_range=time.time()-86400):
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
    current_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    
    # Dictionary for post id, title and time created
    data = {}
    
    # Grabs all submissions from time range
    for submission in submissions:
        time_created = submission.created_utc
        if time_created > time_range:
            data[submission.id] = [submission.title, time_created]

    # Save JSON
    with open(f"../data/raw/posts_{current_time}.json", "w") as json_file:
        json.dump(data, json_file, indent=1)
        print(f"Successfully extracted from r/{sub_name}")

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
            elif currentArg in ("-d", "--day"):
                time_range = time.time()-86400
            elif currentArg in ("-w", "--week"):
                time_range = time.time()-604800
            elif currentArg in ("-m", "--month"):
                time_range = time.time()-2629743
    except getopt.error as err:
        print(str(err))

    # Scrape all posts under listing within time range
    get_raw_data(sub_name, listing, listing_args, time_range)

if __name__ == "__main__":
    main()
