import httpx
from bs4 import BeautifulSoup

async def algorithm(subject, sub):
    toRet = []
    
    # Send a GET request to the URL
    async with httpx.AsyncClient() as client:
        response = await client.get(subject)
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find headlines
        tags = soup.find(id="site-content").find_all("a",href=True)
        print(tags)
        for head in tags:
            h = head.find("h4")
            if h:
                headline = h.get_text()
                toRet.append(headline)

    return toRet

def fix_url(st1):
    st1 = st1
    st2 = ""
    for i in range(0, len(st1) - 1):
        if st1[i:i + 1] == ' ':
            st2 = st2 + '%2'
            continue
        st2 = st2 + st1[i:i + 1]
    return st2

def fix_sub(sub):
    sub = sub.strip()
    sub = sub.replace(" ", "%20")
    return sub

async def startScrapingNews(subject):
    print("Start scraping", subject)

    subject = subject.strip()
    
    url = "https://www.nytimes.com/search?query=" + subject.lower()

    toRet = await algorithm(url, subject)

    return toRet