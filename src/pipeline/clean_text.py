import json
import preprocessing_functions as pf

def main():
    # Load dict of filenames/comments and list of stopwords
    comments = pf.load_comments("raw")
    stopwords = pf.load_stopwords()

    # Clean then save tokens as JSON
    for p, c in comments.items():
        cleaned_comments = []
        for comment in c:
            cleaned_comments.extend(pf.preprocess_comment(comment, stopwords))
        pf.save_tokens(cleaned_comments, p)

if __name__ == "__main__":
    main()
