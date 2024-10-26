# pip install -q -U google-generativeai
import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def summarize(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all headings and paragraphs
        headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        paragraphs = [p.get_text() for p in soup.find_all('p')]

        # Check if there's content to summarize
        if not headings and not paragraphs:
            return "No content available to summarize."

        genai.configure(api_key=os.getenv("GENAI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        try:
            response = model.generate_content(
                """   
                You have been given the task to summarize the following text:
                The response should be in descriptive form, under a single paragraph.
                """ + "\n\n".join(headings + paragraphs),
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=150,
                ),
            )
            return response.text

        except Exception as api_err:
            print(f"An error occurred while generating the summary: {api_err}")
            return "Failed to generate summary."

    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        return {
            "error": "Failed to fetch the webpage. Please check the URL and try again.",
        }
    except Exception as e:
        print(f"An unexpected error occurred while scraping: {e}")
        return {
            "error": "An unexpected error occurred. Please try again later.",
        }
    

# if __name__ == "__main__":
#     url = "https://www.cnn.com/science/vera-rubin-worlds-largest-ca-spc/index.html"
    
#     summary = summarize(url)
#     print("Summary:", summary)