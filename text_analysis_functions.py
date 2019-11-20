from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import string


def only_punctuation(input_string, list_only_punctuation):
    only_symbols = ''
    for char in input_string:
        if char in set(string.punctuation):
            only_symbols += char
    list_only_punctuation.append(only_symbols)

    return list_only_punctuation


def stem_and_lemma(input_string, list_porter_stemmer, list_word_net_lemmatizer):
    wl = WordNetLemmatizer()
    ps = PorterStemmer()

    # Remove punctuations & stopwords, tokenize sentences to words
    translator = str.maketrans('', '', string.punctuation)
    stop_words = set(stopwords.words('english'))

    stem_valid_words, lemma_valid_words = [], []

    temp_word_tokenized = input_string.translate(translator)  # remove punctuations
    temp_word_tokenized = word_tokenize(temp_word_tokenized)  # tokenize sentence into words
    for word in temp_word_tokenized:
        if word not in stop_words:  # remove stop words
            stem = ps.stem(word)  # PorterStemmer
            lemma = wl.lemmatize(word)  # WordNetLemmatizer
            stem_valid_words.append(stem)
            lemma_valid_words.append(lemma)
    list_porter_stemmer.append(stem_valid_words)
    list_word_net_lemmatizer.append(lemma_valid_words)

    return list_porter_stemmer, list_word_net_lemmatizer
