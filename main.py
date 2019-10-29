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
df_Library = pd.DataFrame(data=files, columns=["filename"])
df_Library["path"] = source + "\\" + df_Library["filename"].str[:2] + "\\" + df_Library["filename"]
df_Library["volume"] = df_Library["filename"].str[1]
df_Library = df_Library[["path", "volume"]]

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
    Dune = df_Library[df_Library["volume"] == str(Book)]["path"]
    Chapter = 0

    for html_file in Dune: # Main loop over each chapter
        with open(html_file, encoding="utf8") as markup:
            soup = BeautifulSoup(markup, 'html.parser')

            AllParagraphs = soup.body.find_all(['p', 'blockquote'])
            for row, paragraph in enumerate(AllParagraphs):
                Class = paragraph.attrs['class'][0]
                Text = paragraph.get_text().replace('\n        ', '').replace('\n', '').replace('  ', ' ').replace('  ', ' ') #?!
                if Class == ChapterStarters[Book]: Chapter += 1
                if Class == 'volume': Text = str.upper(Text)

                DuneCronicles.append([Book, Chapter, Class, Text])

# Adjust chapter numbers for 1st pages with volume names
for row, value in enumerate(DuneCronicles):
    if value[1] == 0: DuneCronicles[row][1] = 1

df_DuneCronicles = pd.DataFrame(data=DuneCronicles, columns=['Book','Chapter','Class','Text'])

Duplicates, EmptyLines  = [], []
for row in range(0, len(DuneCronicles)): # range --> enumerate
    # List to handle duplicates in Book 1 where 'blockquote' is a parent to 'noindent'
    # which causes duplicate record for chapter opening quotes
    if (DuneCronicles[row][0] == 1 or DuneCronicles[row][0] == 8) and \
        DuneCronicles[row][2] == 'blockquote':
        Duplicates.append(True)
    else:
        Duplicates.append(False)
    # Empty lines at the begining of each chapter in Book 7 & 8
    if DuneCronicles[row][2] == 'linespace' or \
       DuneCronicles[row][2] == 'right-para' or \
       DuneCronicles[row][2] == 'center-para' or \
       DuneCronicles[row][2] == 'linegroup' or \
       DuneCronicles[row][2][:5] == 'image':
        EmptyLines.append(True)
    else:
        EmptyLines.append(False)

Duplicates.insert(0, False)
Duplicates = Duplicates[0:len(Duplicates)-1]

df_DuneCronicles['Duplicates'] = Duplicates
df_DuneCronicles['EmptyLines'] = EmptyLines

df_DuneCronicles = df_DuneCronicles[df_DuneCronicles['Duplicates'] == False] # Remove duplicates from Book 1
df_DuneCronicles = df_DuneCronicles[df_DuneCronicles['EmptyLines'] == False] # Remove empty lines from Book 7 & 8
df_DuneCronicles.reset_index(drop=True, inplace=True)

Class_Identifiers = pd.read_excel('data\Class_Identifiers.xlsx')

df_DuneCronicles = df_DuneCronicles.merge(Class_Identifiers,
             how='left',
             on=['Book','Class'],
             sort=False)

output_columns = ['Book','Chapter','Class','Identifier_A','Identifier_B','Text']
output_filename = 'output\DuneCronicles.csv'

df_DuneCronicles = df_DuneCronicles[output_columns]
df_DuneCronicles.to_csv(output_filename, index=False, encoding='utf-8')
