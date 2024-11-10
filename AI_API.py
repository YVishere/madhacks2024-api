import google.generativeai as genai


def input_prompt(x):
    genai.configure(api_key="AIzaSyD1KcB-Swnmj7bITFZ4Wbln6rmhS7w9L10")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(x)
    return(response.text)