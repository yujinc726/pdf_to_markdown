import streamlit as st
import tempfile
import os
from agent import convert_pdf_to_markdown

def main():
    st.title("PDF to Markdown Converter")
    st.write("Made by 차유진")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    user_requirements = st.text_area(
        "요구사항 입력",
        value="내용은 수정하지 말고 형식만 올바르게 수정\n강의내용과 무관한 학교명, 저작권 표시, 페이지 번호 등은 무시",
        height=150
    )

    translate = st.checkbox("한국어 번역", value=False)

    if st.button("Convert"):
        if uploaded_file and user_requirements:
            with st.spinner("Converting PDF to Markdown..."):
                # 임시 파일 생성
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_file_path = temp_file.name

                try:
                    # Convert PDF to Markdown
                    markdown_content = str(convert_pdf_to_markdown(temp_file_path, user_requirements, translate))

                    if "Error" in markdown_content:
                        st.error(markdown_content)
                        return

                    # 결과 표시
                    st.subheader("Converted Markdown")
                    st.markdown(markdown_content)

                    # 파일 다운로드 버튼
                    output_filename = f"{os.path.splitext(uploaded_file.name)[0]}.md"
                    markdown_bytes = markdown_content.encode('utf-8')
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