from openai import OpenAI
from agents import Agent, Runner
from document_parser import document_parser
import streamlit as st

openAI_API_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=openAI_API_key)

async def convert_pdf_to_markdown(pdf_path, user_requirements, translate):
    agent = Agent(
    model='gpt-4o',
    name="pdf document parser",
    instructions=f"""
    You are an expert in markdown formatting and document structuring. Your task is to validate and refine the provided markdown content to ensure it is well-structured, accurate, and aligns with the user's requirements. Check for issues like:
    - Incorrect formatting (e.g., broken headings, lists, tables).
    - Missing or unclear content (e.g., incomplete sections, unreadable charts).
    - Inconsistent styles or errors in markdown syntax.
    - Only return the markdown content, no other text or comments.
    - Print the markdown box in the console
    - Don't omit any content that is important
    
    pdf path: {pdf_path}
    User requirements: {user_requirements}
    Translate the content to Korean: {translate}
    
    If the content has errors or doesn't meet the requirements, revise it to improve clarity, structure, and completeness while preserving the original meaning. Provide the refined markdown content as output.
    """,
    tools=[document_parser,])
    
    markdown = await Runner.run(agent, user_requirements)
    return markdown.final_output