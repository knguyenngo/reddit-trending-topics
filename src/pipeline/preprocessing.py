import re, string, json, unicodedata

# Clean comments
def clean(text):
    text = unicodedata.normalize("NFKD", text) # Normalize text
    text = text.lower() # Lowercase text
    text = re.sub(r"\d+", "", text) # Remove numbers
    text = re.sub(r"http\S+", "", text) # Remove links
    text = re.sub(r"[\u2019]", "#'#", text) # Replace middle apostrophe with pattern to save
    text = re.sub(r"(?!#)\W(?!#)", " ", text) # Remove all special chars
    text = re.sub(r"#'#", "'", text) # Revert middle apostrophe back

    return text

def tokenize(text):
    tokens = text.split()
    print(tokens)

#def remove_stopwords(tokens, stopwords):

#def load_stopwords():

#def preprocess_comment(text, stopwords):

def main():
    with open("../data/raw/post_comments/1q8inb4_2026-01-12_1768238336.0916393.json", mode="r", encoding="utf-8") as read_json:
        texts = json.load(read_json)
    for t in texts[:2]:
        t = clean(t)
        tokenize(t)

if __name__ == "__main__":
    main()
