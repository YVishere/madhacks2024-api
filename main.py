from fastapi import FastAPI
import time
from Scraper import startScraping
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
async def scrape_view(subject: str):
    start_time = time.time()
    scraped_data = await startScraping(subject)
    time_taken = time.time() - start_time

    return {'subject': subject, 'time_taken': time_taken, 'data': scraped_data}

@app.get("/")
def home_view():
    return "Hello world"

if __name__ == "__main__":
    uvicorn.run(app)