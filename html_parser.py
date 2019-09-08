from bs4 import BeautifulSoup
import certifi
import urllib3
import pandas as pd
import re

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

url = 'https://storage.googleapis.com/dune_text_analysis_html/D1.html'
response = http.request('GET', url)
soup = BeautifulSoup(response.data, 'html.parser')

title = soup.title.string

paragraph = []
for i in soup.find_all('p'):
    paragraph.append(i)

class_dictionary = {
    "indent" : "text",
    "space-break1" : "text",
    "right" : "opening_caption",
    "space-break" : "opening_caption",
    "blockquote" : "opening_text",
    "noindent" : "opening_text",
    "linegroup" : "text_poem",
    "line" : "text_poem",
    "line1" : "text_poem",
    "linex" : "text_poem"
}

text_part = {}
df_Dune = pd.DataFrame(columns=[
    "volume",
    "book",
    "paragraph"
    "part",
    "text",
    "character"
])

def ExtractText(text):
    s = text

    # Check what's the text part, based on class name and assign unified one based on class_dictionary
    try:
        class_start = s.find("<p class=") + 10
        class_end = s.find(">")-1
        class_type = s[class_start:class_end]
        text_part[i] = class_dictionary[class_type]
    except:
        pass
    
    # Clear text
    s = re.sub("  ", "", str(s))            # Remove spare whitespaces
    s = re.sub("\r\n", "", s)               # Remove line feeds
    s = re.sub("<em>", "‘", str(s))         # Change "thoughts" from cursive to dialogue format
    s = re.sub("</em>", "’", str(s))        # Change "thoughts" from cursive to dialogue format
    s = re.sub("<p class=.*>", "", s)       # Remove class openings 
    s = re.sub("</p>", "", s)               # Remove class endings
    s = re.sub("<a id=.*>", "", s)          # Remove id="page." references
    
    return s;
