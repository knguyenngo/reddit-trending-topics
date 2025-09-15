import json
import time
import requests

FILE_PATH = "../data/raw/main.json"

def process_data(path):
    # Load main page data
    with open(path, "r") as data_file:
        data = json.load(data_file)

    # Get posts data
    data = data[0]
    j_children = data["data"]["children"]
    post_num = 0

    # Grab JSON data of each post
    for i in j_children:
        if i["data"]:
            # Scrapes post title
            # Convert epoch value to readable date format
            # Transform permalink value to link of post
            #page = i["data"]["name"]
            #title = i["data"]["title"]
            #ti = time.ctime(i["data"]["created"])
            link = i["data"]["permalink"] 
            
            # Send request for JSON
            url = f"https://www.reddit.com{link}.json"
            headers = {
                "User-Agent": "testAgent"   
            }

            response = requests.get(url, headers=headers)

            # Retrieve JSON
            if response.status_code == 200:
                new_data = response.json()

                # Add JSON to list
                page_data = []
                page_data.append(new_data)

                # Save JSON
                with open(f"../data/raw/pages/{post_num}.json", "w") as json_file:
                    json.dump(page_data, json_file, indent=1)
                    print(f"Saved {post_num} to JSON")

                # Wait before scraping next page
                time.sleep(2)
            else:
                print("Failed to retrieve page. Status code:", response.status_code)
            post_num += 1

def main():
    process_data(FILE_PATH)

if __name__ == "__main__":
    main()
