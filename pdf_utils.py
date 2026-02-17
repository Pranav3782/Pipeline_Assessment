import pdfplumber

def extract_pages(file_path: str):
    pages = {}

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            pages[i + 1] = text or ""

    return pages
