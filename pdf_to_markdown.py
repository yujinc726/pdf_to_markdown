import streamlit as st
import requests
import os
import json
import tempfile
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from io import BytesIO

# OpenAI 클라이언트 초기화
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. Streamlit Cloud의 Secrets에서 OPENAI_API_KEY를 설정해주세요.")
    st.stop()

openai_client = OpenAI(api_key=api_key)

# Upstage Document AI를 Tool로 정의
@tool
def convert_pdf_to_markdown(filename: str) -> str:
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

# LLM을 사용해 마크다운 검증 및 수정
def refine_markdown_with_llm(markdown_content: str, user_requirements: str) -> str:
    """
    Uses OpenAI LLM to validate and refine markdown content based on user requirements.
    Args:
        markdown_content (str): Initial markdown content.
        user_requirements (str): User's specific requirements for the markdown.
    Returns:
        str: Refined markdown content.
    """
    system_prompt = f"""
    You are an expert in markdown formatting and document structuring. Your task is to validate and refine the provided markdown content to ensure it is well-structured, accurate, and aligns with the user's requirements. Check for issues like:
    - Incorrect formatting (e.g., broken headings, lists, tables).
    - Missing or unclear content (e.g., incomplete sections, unreadable charts).
    - Inconsistent styles or errors in markdown syntax.
    
    User requirements: {user_requirements}
    
    If the content has errors or doesn't meet the requirements, revise it to improve clarity, structure, and completeness while preserving the original meaning. Provide the refined markdown content as output.
    """
    
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the markdown content to refine:\n\n{markdown_content}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# Streamlit UI
def main():
    st.title("PDF to Markdown Converter")
    st.write("by 차유진")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    user_requirements = st.text_area(
        "요구사항 입력",
        placeholder="E.g., '내용은 수정하지 말고, 형식만 올바르게 수정해줘. 강의내용과 무관한 저작권 표시, 페이지 번호 등은 무시해줘. 한국어로 번역해줘.'",
        height=150
    )

    if st.button("Convert"):
        if uploaded_file and user_requirements:
            with st.spinner("Document Parsing..."):
                # 임시 파일 생성
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_file_path = temp_file.name

                try:
                    # Tool 호출로 마크다운 변환
                    initial_markdown = convert_pdf_to_markdown(temp_file_path)

                    if "Error" in initial_markdown:
                        st.error(initial_markdown)
                        return

                    # LLM으로 마크다운 검증 및 수정
                    with st.spinner("Refining markdown with LLM..."):
                        refined_markdown = refine_markdown_with_llm(initial_markdown, user_requirements)

                    # 결과 표시
                    st.subheader("Converted Markdown")
                    st.markdown(refined_markdown)

                    # 파일 다운로드 버튼
                    output_filename = f"{os.path.splitext(uploaded_file.name)[0]}.md"
                    markdown_bytes = refined_markdown.encode('utf-8')
                    st.download_button(
                        label="Download Markdown",
                        data=markdown_bytes,
                        file_name=output_filename,
                        mime="text/markdown"
                    )
                finally:
                    # 임시 파일 삭제
                    try:
                        os.unlink(temp_file_path)
                    except Exception as e:
                        st.warning(f"Could not delete temporary file: {str(e)}")
        else:
            st.warning("Please upload a PDF file and specify requirements.")

if __name__ == "__main__":
    main()