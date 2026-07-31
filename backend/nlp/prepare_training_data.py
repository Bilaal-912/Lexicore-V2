import re
from datasets import load_dataset

def extract_category(question: str) -> str:
    match = re.search(r'related to \"(.+?)\"', question)
    return match.group(1)

def build_classification_dataset(hf_dataset):
    texts = []
    labels = []

    for example in hf_dataset:
        if len(example["answers"]["text"]) == 0:
            continue

        category = extract_category(example["question"])
        clause_text = example["answers"]["text"][0]

        texts.append(clause_text)
        labels.append(category)

    return texts, labels

SELECTED_CATEGORIES = [
    "License Grant", "Cap On Liability", "Audit Rights", "Anti-Assignment",
    "Insurance", "Governing Law", "Post-Termination Services", "Minimum Commitment",
    "Exclusivity", "Revenue/Profit Sharing", "Ip Ownership Assignment",
    "Non-Transferable License", "Termination For Convenience", "Non-Compete",
    "Uncapped Liability"
]

def filter_categories(texts, labels):
    filtered_texts = []
    filtered_labels = []

    for text, label in zip(texts, labels):
        if label in SELECTED_CATEGORIES:
            filtered_texts.append(text)
            filtered_labels.append(label)

    return filtered_texts, filtered_labels

if __name__ == "__main__":
    test_question = 'Highlight the parts (if any) of this contract related to "Document Name" that should be reviewed by a lawyer.'
    print(extract_category(test_question))

    dataset = load_dataset("theatticusproject/cuad-qa", revision="refs/convert/parquet")
    texts, labels = build_classification_dataset(dataset["train"])
    texts, labels = filter_categories(texts, labels)

    from collections import Counter
    print(f"\nFinal dataset size: {len(texts)}")
    print(Counter(labels))