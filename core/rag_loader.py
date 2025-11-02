# core/rag_loader.py
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()
_vectorstore = None

def load_vectorstore():
    global _vectorstore
    if _vectorstore:
        return _vectorstore
    path = "db/study_vector_db"
    if not os.path.exists(path):
        raise FileNotFoundError("Vectorstore not found. Run build_vectorstore.py first.")
    emb = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))
    _vectorstore = FAISS.load_local(path, emb, allow_dangerous_deserialization=True)
    return _vectorstore
