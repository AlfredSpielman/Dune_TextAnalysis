import pandas as pd
from nltk.tokenize import sent_tokenize
from text_analysis_functions import stem_and_lemma, only_punctuation

# Original text
DuneCronicles = pd.read_csv(r'output\DuneCronicles.csv')

# Converting strings to lower case and drop empty lines
DuneCronicles['Text'] = DuneCronicles['Text'].str.lower()
DuneCronicles = DuneCronicles.dropna(subset=['Text'])

# Tokenize text into sentences
sentences = []
for row in DuneCronicles.itertuples():
    for sentence in sent_tokenize(row[6]):
        sentences.append((row[1], row[2], row[3], row[4], row[5], sentence))

cols = ['Book', 'Chapter', 'Class', 'Identifier_A', 'Identifier_B', 'Text']
newDuneCronicles = pd.DataFrame(sentences, columns=cols)

list_porter_stemmer, list_word_net_lemmatizer, list_only_punctuation = [], [], []

for row in newDuneCronicles.itertuples():
    text_to_analyze = row[6]
    only_punctuation(text_to_analyze, list_only_punctuation)
    stem_and_lemma(text_to_analyze, list_porter_stemmer, list_word_net_lemmatizer)

newDuneCronicles['Punctuation'] = list_only_punctuation
newDuneCronicles['PorterStemmer'] = list_porter_stemmer
newDuneCronicles['WordNetLemmatizer'] = list_word_net_lemmatizer

newDuneCronicles.to_csv(r'output\newDuneCronicles.csv', index=False)
