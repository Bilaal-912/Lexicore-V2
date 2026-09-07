import re

def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned_lines = [
        line for line in lines
        if not re.fullmatch(r"\s*-+\s*", line)
        and not line.strip().startswith("Source:")
    ]
    cleaned_text = "\n".join(cleaned_lines)

    cleaned_text = re.sub(r"(?<!\w)-{3,}(?!\w)", "", cleaned_text)
    cleaned_text = normalize_redactions(cleaned_text)

    return cleaned_text

def normalize_redactions(text: str) -> str:
    text = re.sub(r"\[\*+\]\*?", "[REDACTED]", text)
    text = re.sub(r"_{4,}", "[REDACTED]", text)
    return text

def segment_clauses(text: str) -> list[str]:
    pattern = r"\n\s*\d+\.\s+"
    raw_clauses = re.split(pattern, text)
    clauses = [c.strip() for c in raw_clauses if c.strip()]
    return clauses[1:]

if __name__ == "__main__":
    from backend.nlp.pdf_extractor import extract_text_from_pdf

    raw_text = extract_text_from_pdf("data/sample_contract.pdf")
    cleaned = clean_text(raw_text)
    print(cleaned[:1500])
    clauses = segment_clauses(cleaned)
    print(f"Found {len(clauses)} clauses\n")
    for c in clauses[:3]:
        print(c[:200])
        print("---")