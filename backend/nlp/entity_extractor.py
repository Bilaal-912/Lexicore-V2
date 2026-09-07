import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> list[dict]:
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})

    return entities

RELEVANT_LABELS = {"ORG", "PERSON", "DATE", "MONEY", "GPE", "LAW", "PERCENT"}

def extract_relevant_entities(text: str) -> list[dict]:
    doc = nlp(text)
    entities = []
    seen = set()

    for ent in doc.ents:
        if ent.label_ not in RELEVANT_LABELS:
            continue

        cleaned_text = clean_entity_text(ent.text)

        if cleaned_text.lower() in GENERIC_TERM_STOPLIST:
            continue

        key = (cleaned_text, ent.label_)
        if key in seen:
            continue

        seen.add(key)
        entities.append({"text": cleaned_text, "label": ent.label_})

    return entities

GENERIC_TERM_STOPLIST = {
    "agreement", "company", "service", "specifications", "effective date",
    "brand features", "authorized equipment", "acceptance"
}

LEADING_WORDS_TO_STRIP = ["the ", "between ", "a ", "an ", 'the "']

def clean_entity_text(text: str) -> str:
    cleaned = " ".join(text.split())

    for prefix in LEADING_WORDS_TO_STRIP:
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):]

    return cleaned.strip(' "')

def truncate_at_exhibits(text: str) -> str:
    markers = ["EXHIBIT A", "EXHIBIT B", "EXHIBIT C", "SCHEDULE A", "APPENDIX A"]
    earliest_cutoff = len(text)

    for marker in markers:
        idx = text.find(marker)
        if idx != -1 and idx < earliest_cutoff:
            earliest_cutoff = idx

    return text[:earliest_cutoff]

if __name__ == "__main__":
    from backend.nlp.pdf_extractor import extract_text_from_pdf
    from backend.nlp.clause_segmenter import clean_text

    raw_text = extract_text_from_pdf("data/sample_contract.pdf")
    cleaned = clean_text(raw_text)
    truncated = truncate_at_exhibits(cleaned)
    entities = extract_relevant_entities(truncated)
    for e in entities:
        print(e)