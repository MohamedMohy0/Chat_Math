from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

faiss_index_path = "Math_Model.bin"
index = faiss.read_index(faiss_index_path)

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

model = OllamaLLM(model="llama3.2")

def retrieve_context(query, top_k=1):
    """Retrieve the most relevant context from FAISS index."""
    query_embedding = np.array([embed_model.encode(query)], dtype='float32')
    distances, indices = index.search(query_embedding, top_k)
    
    retrieved_texts = []
    for idx in indices[0]:
        if idx != -1: 
            retrieved_texts.append(f"Indexed Text {idx}")
    
    return "\n".join(retrieved_texts) if retrieved_texts else ""

def get_answer(question):
    """Get the answer to a single question using the model and retrieved context."""
    retrieved_context = retrieve_context(question)
    prompt = ChatPromptTemplate.from_template("Context: {context}\nAnswer the following: {text}")
    model_input = prompt.format(context=retrieved_context, text=question)
    model_output = model.invoke(model_input).strip()
    print(model_output)
    return model_output




