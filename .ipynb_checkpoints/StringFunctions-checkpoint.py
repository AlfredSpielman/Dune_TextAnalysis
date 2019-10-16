import re

class_dictionary = {
    "indent" : "text_content",
    "space-break1" : "text_content",
    "right" : "opening_caption",
    "space-break" : "opening_caption",
    "blockquote" : "opening_text",
    "noindent" : "opening_text",
    "linegroup" : "text_poem",
    "line" : "text_poem",
    "line1" : "text_poem",
    "linex" : "text_poem",
    "chapter-title" : "chapter_title",
    "" : ""}

def PartOfText(text):
    # Function to regognize what part of text the given string is
    class_start = text.find("<p class=") + len("<p class=") + 1
    class_end = text.find(">") - 1
    
    if class_start < 10:
        text_part = ""
    else:
        class_type = text[class_start:class_end]
        text_part = class_dictionary[class_type]

    return text_part;


def ExtractText(text):
    # Function to extract just text from given string and remove all html elements
    text = text.strip()
    text = re.sub("<em>", "‘", str(text))         # Change "thoughts" from cursive to dialogue format start
    text = re.sub("</em>", "’", str(text))        # Change "thoughts" from cursive to dialogue format end
    text = re.sub("\r\n", "", text)               # Remove line feeds
    text = re.sub("\n", "", text)                 # Remove line feeds
    text = re.sub("</p>", "", text)               # Remove class endings end
    text = re.sub("<a id=.*>", "", text)          # Remove id="page." references
    text = re.sub("<.*blockquote.*>", "", text)
    text = re.sub("<.*head>", "", text)
    text = re.sub("<.*body>", "", text)
    text = re.sub("<.*title.*>", "", text)
    text = re.sub("<.*link.*>", "", text)
    text = re.sub("<.*meta.*>", "", text)
    text = re.sub("<.*xml.*>", "", text)

    return text;