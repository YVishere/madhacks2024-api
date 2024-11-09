from bs4 import BeautifulSoup
import httpx
import numpy as np

async def algorithm(subject):
    arr = np.array([])
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(subject)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            for p in paragraphs:
                arr.append(p.text)
            return arr
        except AttributeError:
            return arr

def fix_url(st1):
    st1 = st1 + '_'
    st2 = ""
    for i in range(0, len(st1) - 1):
        if st1[i:i + 1] == ' ':
            st2 = st2 + '_'
            continue
        st2 = st2 + st1[i:i + 1]
    return st2

def arr_to_String(arr):
    toRet = ""
    for i in range(0, len(arr)):
        toRet = toRet + arr[i] + " "
    return toRet

async def startScraping(subject):

    print("Start scraping", subject)

    n = subject.find(' ')
    if not n == -1:
        subject = fix_url(subject)

    enable_fArray = True

    if subject.find("https:") != -1:
        url = subject
        enable_fArray = False
    else:    url = "https://en.wikipedia.org/wiki/" + subject

    toRet = await algorithm(url)
    toRet = arr_to_String(toRet)

    return toRet