import json
import preprocessing_functions as pf
import data_utils as ut

def main():
    # Load dict of filenames/comments and list of stopwords
    comments = ut.load_comments("raw")
    stopwords = ut.load_stopwords()

    # Clean then save tokens as JSON
    for p, c in comments.items():
        cleaned_comments = []
        for comment in c:
            cleaned_comments.extend(pf.preprocess_comment(comment, stopwords))
        ut.save_tokens(cleaned_comments, p)

if __name__ == "__main__":
    main()
