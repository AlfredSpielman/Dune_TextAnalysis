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
    "normal" : "text_content",
    "normal-1" : "text_content",
    "normal1" : "text_content",
    "bodytext" : "text_content",
    "bodytext-left" : "text_caption",
    "bodytextb" : "text_content",
    "bodytextt" : "text_content",
    "extract" : "text_poem",
    "extractba" : "text_poem",
    "bodytext-leftz" : "opening_text",
    "bodytext-leftza" : "opening_text",
    "hanging1" : "opening_text",
    "hanging" : "opening_text",
    "extract-indent1" : "opening_text",
    "extract-indent" : "text_poem",
    "bodytext1" : "text_content",
    "extract-indent-a1" : "text_poem",
    "extract-indent-b1" : "text_poem",
    "extract2" : "text_content",
    "extract-3" : "text_poem",
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