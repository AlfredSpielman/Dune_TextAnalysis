import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag, RegexpParser
import string

wl = WordNetLemmatizer()
ps = PorterStemmer()

# Original text
DuneCronicles = pd.read_csv(r'output\DuneCronicles.csv')

# Converting all letters to lower case and drop empty lines
DuneCronicles['Text'] = DuneCronicles['Text'].str.lower()
DuneCronicles = DuneCronicles.dropna(subset=['Text'])

# Tokenize text into sentences
sentences = []
for row in DuneCronicles.itertuples():
    for sentence in sent_tokenize(row[6]):
        sentences.append((row[1], row[2], row[3], row[4], row[5], sentence))

cols = ['Book', 'Chapter', 'Class', 'Identifier_A', 'Identifier_B', 'Text']
newDuneCronicles = pd.DataFrame(sentences, columns=cols)

# Remove punctuations & stopwords, tokenize sentences to words
translator = str.maketrans('', '', string.punctuation)
stop_words = set(stopwords.words('english'))

list_PorterStemmer, list_WordNetLemmatizer = [], []
for row in newDuneCronicles.itertuples():
    stem_valid_words, lemma_valid_words = [], []
    temp_word_tokenized = row[6].translate(translator)  # remove punctuations
    temp_word_tokenized = word_tokenize(temp_word_tokenized)  # tokenize sentence into words
    for word in temp_word_tokenized:
        if word not in stop_words:  # remove stop words
            stem = ps.stem(word)  # PorterStemmer
            lemma = wl.lemmatize(word)  # WordNetLemmatizer
            stem_valid_words.append(stem)
            lemma_valid_words.append(lemma)
    list_PorterStemmer.append(stem_valid_words)
    list_WordNetLemmatizer.append(lemma_valid_words)
