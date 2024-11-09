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

async def algorithm(subject):
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

def fix_array(arr):
    uarr, uind = np.unique(arr, return_index=True)
    uarr = uarr[uind.argsort()]
    return uarr

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

    toRet_preFix = await algorithm(url)
    if enable_fArray: toRet = fix_array(toRet_preFix)

    return toRet.tolist()