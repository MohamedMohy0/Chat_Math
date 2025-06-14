import pandas as pd
import torch
from torch.utils.data import DataLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

data_path =r"D:\Gradution\Final project\preprocissing\train_data\precalculus.xlsx"
df = pd.read_excel(data_path)

def preprocess_data(df):
    """Extract text data from the dataframe."""
    texts = df.iloc[:, 0].astype(str).tolist()  
    return texts

texts = preprocess_data(df)

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = np.array([embed_model.encode(text) for text in texts], dtype='float32')

d = embeddings.shape[1]  
index = faiss.IndexFlatL2(d)
index.add(embeddings)

faiss.write_index(index, "precalculus_model.bin")

model = OllamaLLM(model="llama3.2")

class RagDataset(torch.utils.data.Dataset):
    def __init__(self, texts):
        self.texts = texts
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        return {"text": self.texts[idx]}

dataset = RagDataset(texts)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
for batch in dataloader:
    prompt = ChatPromptTemplate.from_template("Train Llama 3.2 on: {text}")
    inputs = [prompt.format(text=t) for t in batch['text']]
    responses = [model.invoke(input) for input in inputs]
    
    
print("Training complete using Ollama. The model is ready for use.")
