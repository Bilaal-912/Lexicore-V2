from datasets import load_dataset

dataset = load_dataset("theatticusproject/cuad-qa", revision="refs/convert/parquet")
print(dataset)

example = dataset["train"][0]
print(example["question"])
print(example["answers"])
print(example["context"][:300])