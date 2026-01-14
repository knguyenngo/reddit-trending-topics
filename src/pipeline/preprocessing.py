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

# Tokenize into unigrams
def tokenize(text):
    tokens = text.split()
    return tokens

def remove_stopwords(tokens, stopwords):
    tokens = [t for t in tokens if t not in stopwords] # Remove stopwords
    return tokens

def load_stopwords():
    with open("./stopwords.json", mode="r", encoding="utf-8") as read_json:
        stopwords = json.load(read_json)
    return set(stopwords)

#def preprocess_comment(text, stopwords):

def main():
    with open("../data/raw/post_comments/1q8inb4_2026-01-12_1768238336.0916393.json", mode="r", encoding="utf-8") as read_json:
        texts = json.load(read_json)

    stopwords = load_stopwords()

    for t in texts[:2]:
        t = clean(t)
        tokens = tokenize(t)
        tokens = remove_stopwords(tokens, stopwords)

if __name__ == "__main__":
    main()
