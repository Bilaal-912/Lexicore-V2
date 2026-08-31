import nltk
from nltk.tokenize import sent_tokenize
nltk.download("punkt")
nltk.download("punkt_tab")

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summarize_text(text: str, num_sentences: int = 5, max_sentence_words: int = 100) -> str:
    sentences = sent_tokenize(text)
    filtered_sentences = [s for s in sentences if len(s.split()) <= max_sentence_words]
    filtered_text = " ".join(filtered_sentences)

    parser = PlaintextParser.from_string(filtered_text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)

    return " ".join(str(sentence) for sentence in summary_sentences)
if __name__ == "__main__":
    from backend.nlp.pdf_extractor import extract_text_from_pdf
    from backend.nlp.clause_segmenter import clean_text

    raw_text = extract_text_from_pdf("data/sample_contract.pdf")
    cleaned = clean_text(raw_text)

    summary = summarize_text(cleaned, num_sentences=5)
    print(summary)