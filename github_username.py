import os
from dotenv import load_dotenv
import pdfplumber
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")

client = genai.Client(api_key=api_key)

def extract_text_from_pdf(pdf_file_stream):
    text = ""
    with pdfplumber.open(pdf_file_stream) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_company_github_username(pdf_stream):
    text = extract_text_from_pdf(pdf_stream)
    if not text:
        raise ValueError("No text found in PDF")

    prompt = (
        "You are an AI assistant helping extract GitHub usernames from documents.\n"
    "Given the text of a PDF document below, identify the GitHub username(s) of any prominent technology companies mentioned.\n"
    "- Return only the GitHub usernames, separated by commas if there are multiple.\n"
    "- If no GitHub usernames can be found, respond with exactly: Not found\n"
    "- Do not include any explanations or extra text.\n\n"
    f"Document Text:\n{text}"
    )

    response = client.models.generate_content(
        model="gemma-3n-e4b-it",
        contents=prompt
    )
    return response.text.strip() #type: ignore