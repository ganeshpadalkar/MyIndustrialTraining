import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq

# Load environment variables from .env file
load_dotenv()

def process_pdf(file_path):
    """
    Reads the PDF file from the given file path, splits it into chunks,
    generates embeddings, and stores them in a local FAISS database.
    """
    # 1. Load PDF document using PyPDFLoader
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    # 2. Split document into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(pages)
    
    # 3. Create HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 4. Create local FAISS vector store
    db = FAISS.from_documents(chunks, embeddings)
    
    # 5. Save FAISS index locally
    db.save_local("faiss_index")
    return db

def load_vector_store():
    """
    Loads the local FAISS index if it exists.
    """
    if os.path.exists("faiss_index"):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return None

def get_answer(query, db):
    """
    Retrieves the top 5 relevant document chunks and uses Groq's LLM
    to generate an answer based strictly on the context.
    """
    # 1. Perform similarity search to get top 5 relevant chunks
    docs = db.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 2. Define the strict prompt with PDF context
    prompt = f"""You are a helpful assistant answering questions based ONLY on the provided PDF context.

Context:
{context}

Question:
{query}

Rules:
1. Answer the question using ONLY the provided Context.
2. Do NOT make up any information.
3. If the answer is not available in the Context, respond EXACTLY with: "I don't have that information in this PDF."
4. Keep the response short and clear.

Answer:"""

    # 3. Create Groq client
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    
    # 4. Request completion from Groq LLM
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.0  # Keep generation deterministic and factual
    )
    
    # 5. Return the clean generated answer
    return chat_completion.choices[0].message.content.strip()
