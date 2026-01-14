import re, string, json

# Clean comments
def clean(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text) # Remove numbers
    text = re.sub(r'http\S+', '', text) # Remove links
    text = re.sub(r'(?![A-Za-z]\W[A-Za-z])\W', ' ', text) # Remove special chars

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
