import fitz

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text
    
if __name__ == "__main__":
    text = extract_text_from_pdf("data/sample_contract.pdf")
    print(text[:500])