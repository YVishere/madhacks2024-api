from fastapi import FastAPI
import time
from Scraper import startScraping

import uvicorn

app = FastAPI()

@app.get("/scrape")
async def scrape_view(subject: str, result: str, fastScrape: bool = False):
    start_time = time.time()
    scraped_data = await startScraping(subject, result, fastScrape)
    time_taken = time.time() - start_time

    return {'subject': subject, 'result': result, 'time_taken': time_taken, 'data': scraped_data}

@app.get("/")
def home_view():
    return "Hello world"

if __name__ == "__main__":
    uvicorn.run(app)