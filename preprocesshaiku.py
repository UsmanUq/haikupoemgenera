from transformers import GPT2Tokenizer
import torch

# Step 1: Load the formatted dataset
with open("formatted_haiku_dataset.txt", "r", encoding="utf-8") as file:
    dataset = file.read()

# Step 2: Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Ensure that the padding token is set (using eos_token as pad_token)
tokenizer.pad_token = tokenizer.eos_token

# Optional: Add a special token for haikus (e.g., [HAIKU])
if "[HAIKU]" not in tokenizer.get_vocab():
    tokenizer.add_special_tokens({"additional_special_tokens": ["[HAIKU]"]})

# Step 3: Tokenize the dataset
tokens = tokenizer(dataset, return_tensors="pt", truncation=True, padding=True, max_length=512)

# Step 4: Save tokenized dataset
torch.save(tokens, "tokenized_haiku_dataset.pt")

print("Dataset tokenized and saved successfully!")
