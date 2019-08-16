from bs4 import BeautifulSoup
import urllib3
import pandas as pd

http = urllib3.PoolManager()

url = 'https://raw.githubusercontent.com/BartekNowakowski/Dune_TextAnalysis/master/html/D1.html'
response = http.request('GET', url)
soup = BeautifulSoup(response.data, 'html.parser')

title = soup.title.string

paragraph = []
for i in soup.find_all('p'):
    paragraph.append(i)
