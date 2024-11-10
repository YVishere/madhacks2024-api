import google.generativeai as genai
import newsScraper as ns
import time
from Scraper import process_text, startScraping

genai.configure(api_key="AIzaSyD1KcB-Swnmj7bITFZ4Wbln6rmhS7w9L10")
global model
model = genai.GenerativeModel("gemini-1.5-flash")

async def trainModel(x):
    global model
    output = await startScraping(x)
    if output == "": #Nothing to train on
        return
    trimmed_response = ' '.join(output.text.split()[:500])
    training_data = {
        "input":x,
        "output":trimmed_response
    }
    operation = genai.create_tuned_model(
        display_name="fine_tuned_model",
        source_model="models/gemini-1.5-flash-001-tuning",
        epoch_count=20,
        batch_size=4,
        learning_rate=0.001,
        training_data=training_data,
    )
    for status in operation.wait_bar():
        time.sleep(10)  # Check the status every 10 seconds
    
    # Get the result of the tuning operation
    result = operation.result()
    print(result)
    
    # Replace the global model with the fine-tuned model
    model = genai.GenerativeModel(model_name=result.name)

def input_prompt(x):
    global model
    response = model.generate_content(x)
    toRet = process_text(response.text)
    trainModel(x)
    return(toRet)

async def news_handler(x):
    global model
    prompt = "Answer in only in one or two words: What is the subject of the sentence in " + x + "?. Do not add any quotes or punctuation. And the subject must be a place, person or a proper noun."
    response = model.generate_content(prompt)
    articles = await ns.startScrapingNews(response.text)
    s = ""
    for art in articles:
        s = s + art + ";; "
    prompt = "Here is a list of new articles about " + x + ". Read out only 5 of them now, and read the next 5 if you have been asked to in the next prompt and so on: " + s
    response = model.generate_content(prompt)
    toRet = process_text(response.text)
    return(toRet)
