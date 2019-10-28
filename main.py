import os
import pandas as pd
from bs4 import BeautifulSoup

source = r"..\html"
directories = [x[0] for x in os.walk(source)]

# List all files in given directory
files = []
for directory in directories:
    for file in os.listdir(directory):
        if file.endswith(".html") and file[2] == "_" and file[5] != "-":
            files.append(file)

# Create DataFrame with file paths and volume numbers
df = pd.DataFrame(data=files, columns=["filename"])
df["path"] = source + "\\" + df["filename"].str[:2] + "\\" + df["filename"]
df["volume"] = df["filename"].str[1]
df = df[["path", "volume"]]

DuneCronicles = []

ChapterStarters = {
    1:'blockquote',
    2:'blockquote1a',
    3:'extract',
    4:'extract',
    5:'epigraph',
    6:'extracts',
    7:'blockquote',
    8:'blockquote'}

for Book in range(1, 9): # Main loop over each book
    Dune = df[df["volume"] == str(Book)]["path"]
    Chapter = 0

    for html_file in Dune: # Main loop over each chapter
        with open(html_file, encoding="utf8") as markup:
            soup = BeautifulSoup(markup, 'html.parser')

            AllParagraphs = soup.body.find_all(['p', 'blockquote'])
            for row, paragraph in enumerate(AllParagraphs):
                Class = paragraph.attrs['class'][0]
                Text = paragraph.get_text().replace('\n        ', '').replace('\n', '').replace('  ', ' ').replace('  ', ' ') #?!
                if Class == ChapterStarters[Book]: Chapter += 1
                DuneCronicles.append([Book, Chapter, Class, Text])

dfBook = pd.DataFrame(data=DuneCronicles, columns=['Book','Chapter','Class','Text'])

Duplicates, EmptyLines = [], []
for row, value in enumerate(DuneCronicles):
    # List to handle duplicates in Book 1 where 'blockquote' is a parent to 'noindent'
    # which causes duplicate record for chapter opening quotes
    if (value[0] == 1 or value[0] == 8) and value[2] == 'blockquote':
        Duplicates.append(True)
    else:
        Duplicates.append(False)
    # Empty lines at the begining of each chapter in Book 7 & 8
    if value[2][:5] == 'image' or value[2] == 'linespace' or value[2] == 'right-para' or value[2] == 'center-para':
        EmptyLines.append(True)
    else:
        EmptyLines.append(False)

Duplicates.insert(0, False)
Duplicates = Duplicates[0:len(Duplicates)-1]

dfBook['Duplicates'] = Duplicates
dfBook['EmptyLines'] = EmptyLines

dfBook = dfBook[dfBook['Duplicates'] == False] # Remove duplicates from Book 1
dfBook = dfBook[dfBook['EmptyLines'] == False] # Remove empty lines from Book 7 & 8
dfBook.reset_index(drop=True, inplace=True)

dfBook[['Book','Chapter','Class','Text']].to_csv('output\DuneCronicles.csv', index=False, encoding='utf-8')
