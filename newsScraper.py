import httpx
from bs4 import BeautifulSoup
import httpx
import numpy as np

async def algorithm(subject):
    toRet = []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(subject)
            soup = BeautifulSoup(response.text, "html.parser")
            sites = soup.find_all("a", href=True)
            for s in sites:
                nresp = await client.get(s['href'])
                nsoup = BeautifulSoup(fix_url2(nresp.text), "html.parser")
                ns = nsoup.find_all("h1")
                toRet = toRet.append(ns)
            return toRet
        except AttributeError:
            return toRet

# Function to fix URL for query string encoding
def fix_url(st1):
    st1 = st1
    st2 = ""
    for i in range(0, len(st1) - 1):
        if st1[i:i + 1] == ' ':
            st2 = st2 + '%2'
            continue
        st2 = st2 + st1[i:i + 1]
    return st2

def fix_url2(st1):
    st2 = "https://news.google.com"+st1[1:]
    return st2

# def process_text(text):
#     text = text.replace("\n", " ")
#     text = text.replace("  ", " ")
#     text = text.replace("\\\"", "\"")
#     text = text.replace("ⓘ", "")
#     text = text.replace("( )", "")
#     text = text.replace("()", "")

#     #Get rid of square brackets and anything inside them
#     text = re.sub(r'\[.*?\]', '', text)
#     text = ' '.join(text.split())
#     return text

async def startScrapingNews(subject):

    print("Start scraping", subject)

    subject = subject.strip()

    n = subject.find(' ')
    if n != -1:
        subject = fix_url2(subject)
    
    url = "news.google.com/search?q=" + subject

    toRet = await algorithm(url)

    return toRet

