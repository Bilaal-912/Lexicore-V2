import re
from datasets import load_dataset

def extract_category(question: str) -> str:
    match = re.search(r'related to \"(.+?)\"', question)
    return match.group(1)

if __name__ == "__main__":
    test_question = 'Highlight the parts (if any) of this contract related to "Document Name" that should be reviewed by a lawyer.'
    print(extract_category(test_question))