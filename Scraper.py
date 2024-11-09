from bs4 import BeautifulSoup
import httpx
import numpy as np

def dontCheck(url):
    if url.find("#") != -1:
        return True
    if url.find("/wiki/") == -1:
        return True
    if url.find(".jpg") != -1 or url.find(".ogg") != -1 or url.find(".svg") != -1 or url.find(".png") != -1 or url.find(".jpeg") != -1 or url.find(".gif") != -1:
        return True
    if url.find("Help:") != -1 or url.find(":") != -1:
        return True
    if url.find("https") != -1:
        return True
    if url.find("commons") != -1 or url.find("_(identifier)") != -1:
        return True

    return False

async def algorithm(subject, result):
    arr = np.array([])
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(subject)
            soup = BeautifulSoup(response.text, "html.parser")
            tags = soup.find(id="bodyContent").find_all("a")
            for tag in tags:
                s = tag.get('href', None)
                if dontCheck(s):
                    continue
                ns = s[s.rfind("/") + 1:]
                if s.find("https") == -1:
                    s = "https://en.wikipedia.org" + s
                if s.lower() == result.lower():
                    print("Found")
                    break
                arr = np.append(arr, ns)
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

async def algorithm_Fast(subject):
    subject = "https://en.wikipedia.org/wiki/" + subject
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(subject)
            soup = BeautifulSoup(response.text, "html.parser")
            tags = soup.find(id="bodyContent").find_all("a")
            return len(tags)
        except AttributeError:
            return 0

def fix_array(arr):
    uarr, uind = np.unique(arr, return_index=True)
    uarr = uarr[uind.argsort()]
    return uarr

async def startScraping(subject, result, fastScrape=False):
    if fastScrape:
        toRet = await algorithm_Fast(subject)
        return toRet

    print("Start scraping", subject)

    n = subject.find(' ')
    if not n == -1:
        subject = fix_url(subject)

    n = result.find(' ')
    if not n == -1:
        result = fix_url(result)

    url = "https://en.wikipedia.org/wiki/" + subject
    check_url = "https://en.wikipedia.org/wiki/" + result

    toRet_preFix = await algorithm(url, check_url)
    toRet = fix_array(toRet_preFix)

    return toRet.tolist()