import json, time, sys, praw, getopt

options = "f:"
long_options = ["file="]
ID = "REDACTED_ID"
SECRET = "REDACTED_SECRET"
AGENT = "topic-modeler"

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
    current_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    # Gather comments from post ID
    for post_id in post_data.keys():
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=None)
        all_comments = [c.body for c in submission.comments.list()]

        # Save JSON
        with open(f"../data/raw/post_comments/{post_id}_{current_time}.json", "w") as json_file:
            json.dump(all_comments, json_file, indent=1)

def main():
    args = sys.argv[1:]
    file_path = ""

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-f", "--file"):
                file_path = currentVal
    except getopt.error as err:
        print(str(err))
 
    gather_comments(file_path)

if __name__ == "__main__":
    main()
