# GitHub Organization Extractor

This is a simple web application that allows you to upload a PDF document, extract the GitHub username of a company mentioned in the document using Google's Gemma model, and fetch the list of public members from GitHub.

## Features

- Upload a PDF containing a tech company mention.
- Extract the company's GitHub username using Gemini (`gemma-3n-e4b-it`).
- Fetch public members of the GitHub organization.
- Save job results to a local SQLite database.
- View results via a Streamlit-based UI.

## Requirements

- Python 3.8+
- A valid [Google Gemini API Key](https://ai.google.dev/)
- A GitHub token (fine-grained) with read-only org access

## Setup

1. **Clone the repository** and navigate into it.

2. **Create a `.env` file** with:
    ```env
    GOOGLE_API_KEY=your_google_gemini_api_key
    GITHUB_TOKEN=your_github_token
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**
    ```bash
    python app.py
    ```

5. Open your browser and go to [http://localhost:8501](http://localhost:8501) for the Streamlit UI.

## Notes

- Only PDF files are supported.
- All job records are stored in `jobs.db`