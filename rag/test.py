import pandas as pd
import torch
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np

# Load test data
test_data_path = r"D:\Gradution\Final project\preprocissing\test_data\intermediate_algebra_test.xlsx" # Change this to your test file
df_test = pd.read_excel(test_data_path)

def preprocess_test_data(df):
    """Extract input-output pairs from the test dataframe."""
    inputs = df.iloc[:, 0].astype(str).tolist()  # Assuming first column is input
    expected_outputs = df.iloc[:, 1].astype(str).tolist()  # Assuming second column is expected output
    return inputs, expected_outputs

inputs, expected_outputs = preprocess_test_data(df_test)

# Load FAISS index
faiss_index_path = "Math_Model.bin"
index = faiss.read_index(faiss_index_path)

# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load Llama 3.2 model
model = OllamaLLM(model="llama3.2")

def retrieve_context(query, top_k=1):
    """Retrieve the most relevant context from FAISS index."""
    query_embedding = np.array([embed_model.encode(query)], dtype='float32')
    distances, indices = index.search(query_embedding, top_k)
    
    retrieved_texts = [inputs[i] for i in indices[0] if i < len(inputs)]
    return "\n".join(retrieved_texts) if retrieved_texts else ""

def evaluate_model(inputs, expected_outputs):
    """Evaluate the model by comparing predictions with expected outputs."""
    correct = 0
    total = len(inputs)
    similarities = []
    
    for inp, expected in zip(inputs, expected_outputs):
        retrieved_context = retrieve_context(inp)
        prompt = ChatPromptTemplate.from_template("Context: {context}\nAnswer the following: {text}")
        model_input = prompt.format(context=retrieved_context, text=inp)
        model_output = model.invoke(model_input).strip()
        
        # Compute similarity
        emb1 = embed_model.encode(model_output, convert_to_tensor=True)
        emb2 = embed_model.encode(expected, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        similarities.append(similarity)
        
        # Count correct predictions (exact match or high similarity)
        if model_output.lower() == expected.lower() or similarity > 0.65:
            correct += 1
    
    accuracy = correct / total * 100
    avg_similarity = np.mean(similarities)
    return accuracy, avg_similarity

# Run evaluation
accuracy, avg_similarity = evaluate_model(inputs, expected_outputs)

print(f"Model Accuracy: {accuracy:.2f}%")
print(f"Similarity Accuracy: {100*avg_similarity:.4f}%")