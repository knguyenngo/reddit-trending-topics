import json

def gather_posts(path):
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
    
    current_post = []

    for k in data:
        entry = data[k]
        if "data_title" in k or ("body" in k and "html" not in k):
            if entry != "[removed]" and entry != "[deleted]":
                current_post.append(entry)

    return 0, current_post

def main():
    posts = []
    i = 0
    
    while True:
        FILE_PATH = f"../data/clean/flattened/flattened_{i}.json"
        status, current_post = gather_posts(FILE_PATH)
        if status < 0:
            break
        i += 1
        posts.extend(current_post)

    with open("../data/clean/all_posts.json", "w") as json_file:
        json.dump(posts, json_file, indent=1)

if __name__ == "__main__":
    main()
