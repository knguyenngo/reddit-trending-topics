import json
import time
from flatten_json import flatten

def flatten_data(path, i):
    # Load file to flatten
    try:
        with open(path, "r") as post_json:
            data = json.load(post_json)
    # No more files to flatten
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return -1

    main_data = data[0][0]
    comments_data = data[0][1]

    # Flatten then combine post data with comments data
    flattened = flatten(main_data)
    flattened.update(flatten(comments_data))

    # Save flattened JSON
    with open(f"../data/clean/flattened/flattened_{i}.json", "w") as json_file:
        json.dump(flattened, json_file, indent=1)
        return 0

def main():
    i = 0
    while True:
        FILE_PATH = f"../data/raw/pages/{i}.json"
        status = flatten_data(FILE_PATH, i)
        if status < 0:
            break
        i += 1

if __name__ == "__main__":
    main()
