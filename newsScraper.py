import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

async def algorithm(subject, sub):
    toRet = []
    loop = asyncio.get_event_loop()
    
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Run the synchronous driver.get() in an executor
        await loop.run_in_executor(None, driver.get, subject)
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Close the WebDriver
        driver.close()
        
        # Find headlines
        headlines = soup.find_all('a', href=True)
        for head in headlines:
            headline = head.get_text()
            if sub.lower() in headline.lower():
                toRet.append(headline)
        
        return toRet
    except AttributeError:
        return toRet
    finally:
        driver.quit()  # Ensure the driver is quit in case of an exception

def fix_url(st1):
    st1 = st1
    st2 = ""
    for i in range(0, len(st1) - 1):
        if st1[i:i + 1] == ' ':
            st2 = st2 + '%2'
            continue
        st2 = st2 + st1[i:i + 1]
    return st2