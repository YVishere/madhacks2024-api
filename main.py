from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import time
from Scraper import startScraping
from post_data import post_dataMain, delete_data
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
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

        # Post data to MongoDB
        document_id = await post_dataMain(subject, scraped_data)
    except Exception as e:
        return {"error": str(e)}

    return {'subject': subject, 'time_taken': time_taken, 'data': scraped_data, 'document_id': str(document_id)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except WebSocketDisconnect:
        # Handle disconnection
        pass

@app.websocket("/ws/{document_id}")
async def websocket_endpoint_with_id(websocket: WebSocket, document_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except WebSocketDisconnect:
        # Delete the document when the connection is closed
        await delete_data(ObjectId(document_id))

@app.get("/prompt")
async def prompt_view(x: str):
    x = x + " talk about this topic for about 500 words"
    try:
        response = await ai.input_prompt(x)
    except Exception as e:
        return {"error": str(e)}
    
    return {'response': response}

@app.get("/")
def home_view():
    return "Hello world"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)