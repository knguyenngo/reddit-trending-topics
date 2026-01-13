import re, string, json

# Clean comments
def clean(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text) # Remove numbers
    text = re.sub(r'http\S+', '', text) # Remove links
    text = re.sub(r'\W', ' ', text) # Remove special chars

#def tokenize(text):

#def remove_stopwords(tokens, stopwords):

#def load_stopwords():

#def preprocess_comment(text, stopwords):


