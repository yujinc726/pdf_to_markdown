import streamlit as st
import tempfile
import os
from agent import convert_pdf_to_markdown
import asyncio

# 페이지 설정 최적화
st.set_page_config(
    page_title="PDF to Markdown Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "PDF를 마크다운으로 변환하는 도구"
    }
)

async def main():

    # Create two columns with a more balanced ratio
    left_column, right_column = st.columns([2, 3])

    with left_column:
        st.title("PDF to Markdown Converter")
        st.write("Made by 차유진")
        # 입력 컨트롤
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        user_requirements = st.text_area(
            "요구사항 입력",
            value="내용은 수정하지 말고 형식만 올바르게 수정\n강의내용과 무관한 학교명, 저작권 표시, 페이지 번호 등은 무시",
            height=150
        )

        translate = st.checkbox("한국어 번역", value=False)

        convert_button = st.button("Convert", type="primary", use_container_width=True)

    with right_column:
        if convert_button:
            if uploaded_file and user_requirements:
                with st.spinner("Converting PDF to Markdown..."):
                    # 임시 파일 생성
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_file_path = temp_file.name

                    try:
                        # Convert PDF to Markdown
                        markdown_content = str(await convert_pdf_to_markdown(temp_file_path, user_requirements, translate))

                        if "Error" in markdown_content:
                            st.error(markdown_content)
                            return

                        # 결과 표시
                        st.subheader("Converted Markdown")
                        output_filename = f"{os.path.splitext(uploaded_file.name)[0]}.md"
                        markdown_bytes = markdown_content.encode('utf-8')
                        st.download_button(
                            label="Download Markdown",
                            data=markdown_bytes,
                            file_name=output_filename,
                            mime="text/markdown",
                            use_container_width=False
                        )
                        st.markdown(markdown_content)
                        
                    finally:
                        # 임시 파일 삭제
                        try:
                            os.unlink(temp_file_path)
                        except Exception as e:
                            st.warning(f"Could not delete temporary file: {str(e)}")
            else:
                st.warning("Please upload a PDF file and specify requirements.")
        else:
            st.info("변환 버튼을 클릭하면 여기에 결과가 표시됩니다.")

if __name__ == "__main__":
    asyncio.run(main())