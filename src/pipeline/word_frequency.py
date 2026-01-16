import json
import preprocessing as pf
import scrape_functions as sf

def calculate_word_frequency(comments):
    word_freq = {}
    # Count word freq
    for c in comments.values():
        for word in c:
            if word in word_freq:
                word_freq[word] = word_freq[word] + 1
            else:
                word_freq[word] = 1
    # Return dict sorted by frequency
    return dict(sorted(word_freq.items(), key=lambda item: item[1]))

def main():
    comments = pf.load_comments("clean")
    word_freq = calculate_word_frequency(comments)
    
    project_dir = sf.find_project_root()
    save_dir = project_dir / "src" / "data" / "clean"

    with open(f"{save_dir}/word_frequencies.json", "w") as json_file:
        json.dump(word_freq, json_file, indent=1)

if __name__ == "__main__":
    main()
