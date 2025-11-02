import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ---------- Paths ----------
base_dir = os.path.dirname(__file__)

# Two markdown files
markdown_files = [
    os.path.join(base_dir, "..","markdown_data" ,"ML-study-assistance.md"),
    os.path.join(base_dir, "..", "markdown_data", "Python_Programming_study_assistance.md"),
]

# Output vector DB directory
db_path = os.path.join(base_dir, "vector_db")

# ---------- Combine and Read ----------
texts = []
for file_path in markdown_files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            texts.append(f.read())
    else:
        print(f"File not found: {file_path}")

if not texts:
    raise FileNotFoundError("No markdown files found. Check your paths!")

# ---------- Split Text ----------
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = splitter.create_documents(texts)

# ---------- Create Embeddings ----------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)

# ---------- Build & Save Vector Store ----------
if docs:
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(db_path)
    print(f"Vector store created successfully at: {db_path}")
else:
    print("No documents to embed.")
