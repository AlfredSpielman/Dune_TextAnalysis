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
<<<<<<< HEAD
df["item"] = df["filename"].str[3:5]
df["path"] = source + "\\" + df["folder"] + "\\" + df["filename"]
df = df[["path", "filename", "folder", "volume", "item"]]

D1 = df[df["volume"] == "1"]["path"]

content = []
for file in D1:
    with open(file, mode="r", encoding="UTF-8") as f:
        content.append(f.readlines())

book = []
for k in range(0, len(content)):
    for i in range(0, len(content[k])):
        book.append(content[k][i])

book_classified = []
for i in range(1, len(book)):
    temp = ["",""]
    s = ExtractText(book[i])
    temp[0] = PartOfText(s)
    temp[1] = re.sub("<p class=.*>", "", s)
    book_classified.append(temp)

book_condensed = ["",""]
for i in range(0, len(book_classified)):
    temp = ["",""]
    if book_classified[i][1] != "":
        temp = [book_classified[i][0], book_classified[i][1]]
        book_condensed.append(temp)
del book_condensed[:2]

# Transfort book_condensed list into DataFrame
df_book_long = pd.DataFrame(book_condensed, columns=["part","content"])

# Get running count, concatenation and filtering column
df_book_long['content'] = df_book_long['content'] + ' '
df_book_long['chapter_count'] = df_book_long.groupby(df_book_long.part.eq('opening_caption').cumsum()).cumcount() + 1
df_book_long['line_count'] = df_book_long.groupby(df_book_long.part.ne('').cumsum()).cumcount() + 1
df_book_long['text_content'] = df_book_long.groupby(df_book_long.part.ne('').cumsum()).content.apply(lambda x : x.cumsum())
df_book_long['take'] = df_book_long['line_count'] == df_book_long.groupby(df_book_long.part.ne('').cumsum())['line_count'].transform('max')
df_book_long['text_part'] = df_book_long.groupby(df_book_long.part.ne('').cumsum()).part.apply(lambda x : x.cumsum())

df_book = df_book_long[df_book_long['take'] == True].reset_index()
df_book = df_book[['text_part', 'content', 'chapter_count']]

df_book['chapter_start'] = df_book['chapter_count'].apply(lambda x : x == 1)
df_book['chapter_num'] = df_book['chapter_start']
df_book['chapter_num'].replace({True:1, False:0}, inplace=True)
df_book['chapter'] = df_book.chapter_num.cumsum() -1
df_book['chapter'] = df_book['chapter'].shift(-1).ffill()

df_book = df_book[['chapter', 'text_part', 'content']][1:]

df_book['opening_caption'] = df_book['content'].str[0] == "—"

df_book['text_content'] = df_book['opening_caption'].shift(-2).ffill() != False
df_book['opening_text'] = df_book['opening_caption'].shift(-1).ffill() != False
df_book['text_content'] = df_book['opening_caption'].shift(1).ffill() != False

text_content_arr = np.where(df_book['text_content'] == True)
for i in text_content_arr:
    df_book['text_part'].iloc[i] = 'text_content'

opening_caption_arr = np.where(df_book['opening_caption'] == True)
for i in opening_caption_arr:
    df_book['text_part'].iloc[i] = 'opening_caption'

opening_text_arr = np.where(df_book['opening_text'] == True)
for i in opening_text_arr:
    df_book['text_part'].iloc[i] = 'opening_text'

df_book['paragraph'] = df_book.groupby(df_book.opening_text.eq(True).cumsum()).cumcount() + 1

df_book.to_csv(r'output/D1.csv',
            index=False,
            columns=['chapter', 'paragraph', 'text_part', 'content'])
=======
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
            for paragraph in range(0, len(AllParagraphs)):
                Class = AllParagraphs[paragraph].attrs['class'][0]
                Text = AllParagraphs[paragraph].get_text().replace('\n        ', '').replace('\n', '').replace('  ', ' ').replace('  ', ' ') #?!
                if Class == ChapterStarters[Book]: Chapter += 1
                DuneCronicles.append([Book, Chapter, Class, Text])

dfBook = pd.DataFrame(data=DuneCronicles, columns=['Book','Chapter','Class','Text'])

Duplicates, EmptyLines = [], []
for row in range(0, len(DuneCronicles)):
    # List to handle duplicates in Book 1 where 'blockquote' is a parent to 'noindent'
    # which causes duplicate record for chapter opening quotes
    if (DuneCronicles[row][0] == 1 or DuneCronicles[row][0] == 8) and DuneCronicles[row][2] == 'blockquote':
        Duplicates.append(True)
    else:
        Duplicates.append(False)
    # Empty lines at the begining of each chapter in Book 7 & 8
    if DuneCronicles[row][2][:5] == 'image' or DuneCronicles[row][2] == 'linespace' or DuneCronicles[row][2] == 'right-para' or DuneCronicles[row][2] == 'center-para':
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
>>>>>>> Messiah_Parser
