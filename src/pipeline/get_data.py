import os, time, sys, getopt, praw
from dotenv import load_dotenv
import scrape_functions as sf
import data_utils as ut

# Secrets for PRAW
load_dotenv()
ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_CLIENT_SECRET")
AGENT = os.getenv("REDDIT_USER_AGENT", "topic-modeler")

# Options for scrape
options = "s:nhtcl:f:u:"
long_options = ["subreddit=", "new", "hot", "controversial", "top", "limit=", "from-hours=", "until-hours="]

def main():
    # Save all data to raw data directory
    data_dir = ut.find_project_root() / "src" / "data"

    # Reddit instance
    reddit = praw.Reddit(
        client_id=ID,
        client_secret=SECRET,
        user_agent=AGENT
    )

    # Parameters for current scrape
    scrape_config = {
            "praw_instance" : reddit,
            "subreddit": "",
            "listing": "new",
            "listing_args": {"limit": 100},
            "from_hours": 72,
            "until_hours": 0,
            "data_dir": data_dir / "raw",
            "current_date": time.strftime("%Y-%m-%d", time.localtime(time.time())),
            "current_time": time.time()
    }

    # Read in arguments
    args = sys.argv[1:]

    # Parse options and values
    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-s", "--subreddit"):
                scrape_config["subreddit"] = currentVal
            elif currentArg in ("-n", "--new"):
                scrape_config["listing"] = "new"
            elif currentArg in ("-h", "--hot"):
                scrape_config["listing"] = "hot"
            elif currentArg in ("-t", "--top"):
                scrape_config["listing"] = "top"
            elif currentArg in ("-c", "--controversial"):
                scrape_config["listing"] = "controversial"
            elif currentArg in ("-l", "--limit"):
                scrape_config["listing_args"] = {"limit": int(currentVal)}
            elif currentArg in ("-f", "--from-hours"):
                scrape_config["from_hours"] = int(currentVal)
            elif currentArg in ("-u", "--until-hours"):
                scrape_config["until_hours"] = int(currentVal)
    except getopt.error as err:
        print(str(err))

    # Validate required arguments
    if not scrape_config["subreddit"]:
        print("Error: Subreddit is required. Use -s or --subreddit")
        sys.exit(1)

    # Scrape all posts under listing within time range
    data_objects, post_data = sf.get_raw_data(scrape_config)
    # Gather comments from post dict
    sf.gather_comments(data_objects, scrape_config)

    # Meta data for current scrape
    meta_data = sf.generate_meta_data(post_data, scrape_config)
    sub_name, current_time = scrape_config["subreddit"], scrape_config["current_time"]

    # Load log file and append meta dict for current scrape
    scrape_logs = ut.load_data("scrape_logs.json", data_dir)
    scrape_logs[f"{sub_name}_{current_time}"] = meta_data
    ut.save_data(scrape_logs, "scrape_logs.json", data_dir)

if __name__ == "__main__":
    main()
