import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')

nltk.download('punkt')


def filter_string(text):
    text_tokens = word_tokenize(text)

    text_without_stopwords = [word for word in text_tokens if not word in stopwords.words()]

    filtered_string = re.sub(r'[^\w\s]', '', str(text_without_stopwords))

    return filtered_string.lower()
