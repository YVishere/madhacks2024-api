import google.generativeai as genai
import newsScraper as ns
from Scraper import process_text


def input_prompt(x):
    genai.configure(api_key="AIzaSyD1KcB-Swnmj7bITFZ4Wbln6rmhS7w9L10")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(x)
    return(response.text)

async def news_handler(x):
    genai.configure(api_key="AIzaSyD1KcB-Swnmj7bITFZ4Wbln6rmhS7w9L10")
    model = genai.GenerativeModel("gemini-1.5-flash")
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
