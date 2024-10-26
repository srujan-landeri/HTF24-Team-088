import google.generativeai as genai

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

def scrape(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    paragraphs = [p.get_text() for p in soup.find_all('p')]

    return headings, paragraphs

def summarize(scraped_content):

    headings, paragraphs = scraped_content
    genai.configure(api_key=os.getenv("GENAI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        """   
            You have been given the task to summarize the following text:
            the response should be in descriptive form, under single paragraph.
        """ 
        + "\n\n".join(headings + paragraphs),
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=150,
        ),
    )

    return response.text

content = scrape("https://www.cnn.com/science/vera-rubin-worlds-largest-camera-spc/index.html")
summary = summarize(content)

print(summary)