import streamlit as st
import requests
import json

API_URL = "http://localhost:5000/upload"

st.set_page_config(page_title="GitHub Org Extractor", layout="centered")
st.title("📄 GitHub Organization Extractor from PDF")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    st.info("Processing... Please wait.")
    with st.spinner("Calling backend API..."):

        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
        try:
            response = requests.post(API_URL, files=files)
            result = response.json()

            if response.status_code == 200:
                st.success("✅ Extraction successful!")

                st.write(f"**Job ID:** `{result['job_id']}`")
                st.write(f"**GitHub Username:** `{result['github_username']}`")

                members = result.get("public_members", [])
                st.write(f"**Public Members** ({len(members)} found):")
                st.code("\n".join(members) if members else "None")

            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")

        except Exception as e:
            st.exception(f"Request failed: {e}")