import json

def gather_comments(path):
    # Load data
    try:
        with open(path, "r") as flattened_list:
            data = json.load(flattened_list)
    # No more posts
    except FileNotFoundError:
        print(f"File not found: {path}")
        return -1, None
    # Decoding error
    except json.decoder.JSONDecodeError as e:
        print(f"JSON decode error in file: {path}")
        print(f"Error: {e}")
        return -1, None

    post_comments = {}
    post_title = ""

    for k in data:
        entry = data[k]
        # Get title of post and initialize k, v for post in dict
        if "data_title" in k and entry != post_title:
            post_title = entry
            post_comments[post_title] = []
        # Add post as key and add comment to list value
        if "body" in k and "html" not in k:
            comments = post_comments[post_title]
            comments.append(entry)

    return 0, post_comments

def main():
    main = {}
    i = 0
    
    # Add dictionary of post with comments to main dictionary
    while True:
        FILE_PATH = f"../data/clean/flattened/flattened_{i}.json"
        status, post_dic = gather_comments(FILE_PATH)
        if status < 0:
            break
        i += 1
        main.update(post_dic)
    
    # Save dictionary of posts mapped to comments to JSON
    with open("../data/clean/posts_comments.json", "w") as json_file:
        json.dump(main, json_file, indent=1)

if __name__ == "__main__":
    main()
