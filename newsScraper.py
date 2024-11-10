import requests
from bs4 import BeautifulSoup
import urllib.parse

# Function to fetch headlines using ScrapingBee API
def algorithm(subject, sub, scrapingbee_url, api_key):
    toRet = []
    
    # Prepare the URL for ScrapingBee API (headless Chrome)
    url = f"{scrapingbee_url}/scrape?api_key={api_key}"
    
    # Prepare the payload (e.g., the URL you want to scrape)
    payload = {
        'url': subject,
        'render': 'true',  # Use JavaScript rendering
        'wait': '3',  # Wait for 3 seconds to allow content to load
    }

    # Send a GET request to the ScrapingBee API
    response = requests.get(url, params=payload)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Find headlines in the page
        headlines = soup.find_all('a', href=True)
        for head in headlines:
            headline = head.get_text()
            if sub.lower() in headline.lower():
                toRet.append(headline)

    return toRet

# Function to fix URL for query string encoding
def fix_url(st1):
    return urllib.parse.quote(st1)

# Function to initiate the scraping process
def start_scraping_news(subject, scrapingbee_url =  "https://app.scrapingbee.com", api_key="GB7RCI4D3JBI9GCCNGDOG5L2J5K3E0HVSOVW1UDIIWVZKTLGH067EYYULAJ4D4HASRHHDNXU268WWKNQ"):
    print("Start scraping", subject)

    subject = subject.strip()

    n = subject.find(' ')
    if not n == -1:
        subject = fix_url(subject)
    
    url = "https://news.google.com/search?q=" + subject

    toRet = algorithm(url, subject, scrapingbee_url, api_key)

    return toRet

