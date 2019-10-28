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

dfDuneCronicles = pd.DataFrame(data=DuneCronicles, columns=['Book','Chapter','Class','Text'])

Duplicates, EmptyLines  = [], []
for row in range(0, len(DuneCronicles)): # range --> enumerate
    # List to handle duplicates in Book 1 where 'blockquote' is a parent to 'noindent'
    # which causes duplicate record for chapter opening quotes
    if (DuneCronicles[row][0] == 1 or DuneCronicles[row][0] == 8) and DuneCronicles[row][2] == 'blockquote':
        Duplicates.append(True)
    else:
        Duplicates.append(False)
    # Empty lines at the begining of each chapter in Book 7 & 8
    if DuneCronicles[row][2][:5] == 'image' or DuneCronicles[row][2] == 'linespace' or DuneCronicles[row][2] == 'right-para' or DuneCronicles[row][2] == 'center-para' or DuneCronicles[row][2] == 'linegroup':
        EmptyLines.append(True)
    else:
        EmptyLines.append(False)

Duplicates.insert(0, False)
Duplicates = Duplicates[0:len(Duplicates)-1]

dfDuneCronicles['Duplicates'] = Duplicates
dfDuneCronicles['EmptyLines'] = EmptyLines

dfDuneCronicles = dfBook[dfBook['Duplicates'] == False] # Remove duplicates from Book 1
dfDuneCronicles = dfBook[dfBook['EmptyLines'] == False] # Remove empty lines from Book 7 & 8
dfDuneCronicles.reset_index(drop=True, inplace=True)

Class_Identifiers = pd.read_excel('data\Class_Identifiers.xlsx')

dfDuneCronicles = dfBook.merge(Class_Identifiers,
             how='left',
             on=['Book','Class'],
             sort=False)

dfDuneCronicles[['Book','Chapter','Class','Identifier_A','Identifier_B','Text']].to_csv('output\DuneCronicles.csv', index=False, encoding='utf-8')
