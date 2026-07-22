import re

def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned_lines = [line for line in lines if not re.fullmatch(r"\s*-+\s*", line)]
    return "\n".join(cleaned_lines)

if __name__ == "__main__":
    from backend.nlp.pdf_extractor import extract_text_from_pdf

    raw_text = extract_text_from_pdf("data/sample_contract.pdf")
    cleaned = clean_text(raw_text)
    print(cleaned[:1500])