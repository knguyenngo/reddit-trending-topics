import json
import requests
import time

# Input: Sub name, listing (hot, new..), total posts to grab, ending post id (for pagination)
# Output: Save raw .JSON to /data/raw/
def get_raw_data(subreddit, listing, post_count, post_id):
    # URL and header
    url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={post_count}&after={post_id}" 
    # Identifier 
    headers = {
        "User-Agent": "testAgent"   
    }
    
    # Sent a request
    response = requests.get(url, headers=headers)

    # Retrieve .json
    if response.status_code == 200:
        new_data = response.json()
        try:
            with open("../data/raw/main.json", "r") as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = []

        # Add to existing data
        existing_data.append(new_data)

        ## Save JSON
        with open("../data/raw/main.json", "w") as json_file:
            json.dump(existing_data, json_file, indent=1)
            print("New data appended to JSON")
            return new_data["data"]["after"], new_data["data"]["children"][-1]
    else:
        print("Failed to retrieve page. Status code:", response.status_code)
        return -1, None

def main():
    ## Options for URL
    subreddit = "MMA"
    listing = "new" # hot, new, best, top
    post_id = "" # New page appear after this post
    stop = time.time()-86400
    posts = set()

    ## Scrape all posts from LAST 24 HOURS
    ## now - 86400 seconds = LAST 24 HOURS
    ## now - 604800 seconds = LAST WEEK
    while True:
        post_id, last_post = get_raw_data(subreddit, listing, 100, post_id)
        if post_id == -1:
            break
        if last_post["data"]["created"] < stop:
            break
        if post_id in posts:
            break
        posts.add(post_id)

if __name__ == "__main__":
    main()
