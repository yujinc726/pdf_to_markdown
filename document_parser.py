import streamlit as st
from agents import function_tool
import requests

@function_tool
def document_parser(filename: str) -> str:
    """
    Converts a PDF file to markdown using Upstage Document AI.
    Args:
        filename (str): Path to the PDF file.
    Returns:
        str: Markdown content as a string or error message if conversion fails.
    """
    try:
        api_key = st.secrets.get("UPSTAGE_API_KEY")
        if not api_key:
            return "Error: UPSTAGE_API_KEY not found in secrets"
            
        url = "https://api.upstage.ai/v1/document-ai/document-parse"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        with open(filename, "rb") as file:
            files = {"document": file}
            data = {
                "ocr": "force",
                "coordinates": True,
                "chart_recognition": True,
                "output_formats": "['markdown']",
                "model": "document-parse"
            }
            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()
            return response.json()['content']['markdown']
    except Exception as e:
        return f"Error converting PDF to markdown: {str(e)}"