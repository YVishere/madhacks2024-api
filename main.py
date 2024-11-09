from fastapi import FastAPI
import time
from Scraper import startScraping

app = FastAPI()

@app.get("/scrape")
def scrape_view(subject: str, result: str, fastScrape: bool = False):
    start_time = time.time()
    scraped_data = startScraping(subject, result, fastScrape)
    time_taken = time.time() - start_time

    return {'subject': subject, 'result': result, 'time_taken': time_taken, 'data': scraped_data}