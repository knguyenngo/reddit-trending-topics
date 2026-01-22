import re, unicodedata

# Clean comments
def clean(text):
    text = unicodedata.normalize("NFKD", text) # Normalize text
    text= text.lower() # Lowercase text
    text = re.sub(r"\d+", "", text) # Remove numbers
    text = re.sub(r"http\S+", "", text) # Remove links
    text = re.sub(r"[\u2019]|'", "#'#", text) # Replace middle apostrophe with pattern to save
    text = re.sub(r"(?!#)\W(?!#)", " ", text) # Remove all special chars
    text = re.sub(r"#'#", "'", text) # Revert middle apostrophe back
    text = re.sub(r"#", " ", text) # Remove ignored #
    return text

# Tokenize into unigrams
def tokenize(text):
    tokens = text.split()
    return tokens

# Remove stopwords from list of tokens
def remove_stopwords(tokens, stopwords):
    return [t for t in tokens if t not in stopwords] # Remove stopwords

# Clean and tokenize text
def preprocess_comment(text, stopwords):
    text = clean(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens, stopwords)
    return tokens

