# PDF to Markdown Converter

PDF 파일을 마크다운으로 변환하는 Streamlit 애플리케이션입니다.

## 기능

- PDF 파일을 마크다운으로 변환
- OpenAI API를 사용한 마크다운 검증 및 수정
- 사용자 요구사항에 따른 마크다운 커스터마이징

## 설치 및 실행 방법

1. 저장소 클론
```bash
git clone [repository-url]
cd [repository-name]
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가합니다:
```
OPENAI_API_KEY=your_openai_api_key
```

4. 애플리케이션 실행
```bash
streamlit run markdown.py
```

## Streamlit Cloud 배포 방법

1. [Streamlit Cloud](https://streamlit.io/cloud)에 가입합니다.
2. GitHub 계정과 연동합니다.
3. "New app" 버튼을 클릭합니다.
4. 저장소, 브랜치, 메인 파일 경로를 선택합니다.
5. "Deploy" 버튼을 클릭합니다.
6. 환경 변수 설정에서 `OPENAI_API_KEY`를 추가합니다.

## 주의사항

- OpenAI API 키는 반드시 비공개로 유지해야 합니다.
- PDF 파일 크기에 따라 변환 시간이 달라질 수 있습니다.

## Features

- Upload PDF files and convert them to Markdown
- Customize the system prompt to control how the AI processes the PDF
- Download the converted Markdown file
- Handles large PDFs by processing them in chunks

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the `.env.example` template and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run markdown.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)
3. Upload a PDF file
4. (Optional) Customize the system prompt
5. Click "Convert to Markdown"
6. Copy the Markdown output or download it as a file

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies listed in requirements.txt

## Notes

- The application processes PDFs in chunks to handle OpenAI's token limits
- The quality of the conversion depends on the PDF's structure and the system prompt
- Make sure your OpenAI API key has sufficient credits for the conversion 