# Smart Learning Assistant

An intelligent **study assistant** built with **Django**, **RAG (Retrieval-Augmented Generation)**, and **Machine Learning**.  
It helps analyze student learning patterns and provides context-aware responses using your own markdown and CSV data.

---

## Features

### RAG (Retrieval-Augmented Generation)
- Uses **LangChain**, **FAISS**, and **OpenAI embeddings**.
- Loads knowledge base from your markdown files (e.g., `markdown_data/Python_Programming_study_assistance.md`).
- Builds vector embeddings and retrieves context-aware answers.

### ML Analytics
- Analyzes user learning data stored in CSVs (`study_user_data.csv`, `user_learning_profile.csv`).
- Computes **weakness scores** and **difficulty clusters**.
- Returns personalized study recommendations.

### Django REST APIs
- `/rag-query/` → Ask questions based on markdown knowledge.
- `/analyze-study/` → Analyze learning data and get weak topics.
- Includes register/login system with **JWT authentication**.

# Contribution
All improvements, big or small, are welcome — whether it’s enhancing functionality, fixing bugs, or adding new features.



