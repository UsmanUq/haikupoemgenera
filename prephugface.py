from torch.utils.data import Dataset, DataLoader
import torch

# Step 1: Load the tokenized dataset
tokens = torch.load("tokenized_haiku_dataset.pt")

# Step 2: Create a custom Dataset class
class HaikuDataset(Dataset):
    def __init__(self, tokens):
        self.input_ids = tokens['input_ids']
        self.attention_mask = tokens['attention_mask']

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.input_ids[idx]  # labels are same as input_ids for language modeling
        }

# Step 3: Create a DataLoader
train_dataset = HaikuDataset(tokens)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

# Check data loader
for batch in train_loader:
    print(batch)
    break
