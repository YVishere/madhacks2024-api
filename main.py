from fastapi import FastAPI
import time
from Scraper import startScraping
# from post_data import post_dataMain
from fastapi.middleware.cors import CORSMiddleware
# from bson import ObjectId
import AI_API as ai

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
    try:
        start_time = time.time()
        scraped_data = await startScraping(subject)
        time_taken = time.time() - start_time

        # # Post data to MongoDB
        # document_id = await post_dataMain(subject, scraped_data)
        document_id = "123"
    except Exception as e:
        return {"error": str(e)}

    return {'subject': subject, 'time_taken': time_taken, 'data': scraped_data, 'document_id': str(document_id)}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             #do nothing
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         # Handle disconnection
#         pass

# @app.websocket("/ws/{document_id}")
# async def websocket_endpoint_with_id(websocket: WebSocket, document_id: str):
#     await websocket.accept()
#     try:
#         while True:
#             #Do nothing
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         # Delete the document when the connection is closed
#         await delete_data(ObjectId(document_id))

@app.get("/prompt")
async def prompt_view_init(x: str):
    x = "Tell me everything you know about " + x + " in 500 words."
    try:
        response = ai.input_prompt(x)
    except Exception as e:
        return {"error": str(e)}
    
    return {'response': response}

@app.get("/")
def home_view():
    return "Hello world"

@app.get("/conv")
async def conv_view(n: str):
    newsFlag = ["news", "article", "articles", "newspaper", "newspapers", "headlines", "headline", "news headlines", "news headline", "news articles", "news article", "news paper", "news papers"]
    if (len(str.split(n)) == 1):
        return prompt_view_init(n)
    for flag in newsFlag:
        if flag in n:
            return news_view(n)
    try:
        response = await ai.news_handler(n)
    except Exception as e:
        return {"error": str(e)}
    
    return {'response': response}

@app.get("/news")
async def news_view(n: str):
    try:
        start_time = time.time()
        scraped_data = await ai.news_handler(n)
        time_taken = time.time() - start_time
    except Exception as e:
        return {"error": str(e)}
    
    return {'subject': n, 'time_taken': time_taken, 'data': scraped_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)