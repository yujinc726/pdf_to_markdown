import streamlit as st
import tempfile
import os
from agent import convert_pdf_to_markdown
import asyncio
from streamlit_gsheets import GSheetsConnection
import pandas as pd

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
    st.title("PDF to Markdown Converter")
    # Create two columns with a more balanced ratio
    left_column, right_column = st.columns([2, 3])
    
    with left_column:
        
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

        st.subheader("감사의 편지 보내기")
        message = st.text_area("감사의 편지를 입력하세요", height=150)
        send_button = st.button("보내기", type="primary", use_container_width=True)
        conn = st.connection("gsheets", type=GSheetsConnection)
        if send_button and message.strip():
            df = conn.read(worksheet="Sheet1", ttl=0)  # 캐시 없이 최신 데이터 가져오기
            if df.empty or "Message" not in df.columns:
                df = pd.DataFrame({"Message": []})  # 빈 데이터프레임 초기화
                
            # 새 메시지 추가
            new_row = {"Message": message}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Google Sheets에 업데이트
            conn.update(worksheet="Sheet1", data=df)
            st.success("편지가 저장되었습니다!")
        elif send_button:
            st.warning("내용을 입력해주세요!")

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