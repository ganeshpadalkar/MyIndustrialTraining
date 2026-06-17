<<<<<<< HEAD
# 📄 PDF Chatbot

A simple, local, and beginner-friendly RAG (Retrieval-Augmented Generation) Chatbot built with Python, LangChain, Streamlit, and Groq. 

## Features

- **Ingestion**: Reads PDFs using LangChain's `PyPDFLoader` and splits them with `RecursiveCharacterTextSplitter`.
- **Embeddings**: Creates semantic representation with HuggingFace's `sentence-transformers/all-MiniLM-L6-v2` model.
- **Local Database**: Stores vector embeddings locally using the `FAISS` library (no cloud storage like Pinecone required).
- **RAG QA System**: Finds the top 5 most relevant content segments to answer queries.
- **Factuality Rules**: Restricts the LLM (llama-3.1-8b-instant on Groq) to answer strictly from the document. If the information isn't present, it returns: `"I don't have that information in this PDF."`
- **Modern UI**: Styled with a premium dark-mode glassmorphic theme.

---

## Project Structure

```text
pdf-chatbot/
│
├── app.py              # Streamlit Web App Frontend
├── rag_pipeline.py     # RAG Pipeline Logic (LangChain, FAISS, Groq)
├── .env                # API Keys and Environment configuration
├── requirements.txt    # Python library dependencies
└── README.md           # Instructions and documentation
```

---

## Setup & Running Instructions

### 1. Prerequisite
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Open your command prompt or terminal, navigate to the `pdf-chatbot` directory, and install the libraries:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Make sure the `.env` file in the project folder contains your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Chatbot
Launch the Streamlit web application:
```bash
streamlit run app.py
```
This will open the application in your default web browser (typically at `http://localhost:8501`).
=======
name : ganesh padalkar
cummins college
hi
>>>>>>> e8e08239feadaa225375e6b6433f0693274a1032
