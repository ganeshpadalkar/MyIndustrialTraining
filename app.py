import os
import tempfile
import streamlit as st
from rag_pipeline import process_pdf, load_vector_store, get_answer

# Set Streamlit page settings
st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Premium dark glassmorphic styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0f19;
    }
    ::-webkit-scrollbar-thumb {
        background: #1f253b;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #2b3352;
    }

    /* Main container background */
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at 50% 0%, #171d37 0%, #090a10 100%) !important;
        color: #e5e7eb !important;
    }
    
    /* Header / Title styling */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        letter-spacing: -0.5px !important;
    }

    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #9ca3af;
        margin-top: -1.5rem;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    /* Box container for premium look */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
    }
    
    /* Style buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #0c0e17 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5) !important;
        color: #0c0e17 !important;
    }
    
    .stButton>button:active {
        transform: translateY(0) !important;
    }

    /* Style Text inputs */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #e0e0e0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input::placeholder {
        color: #b0b0b0 !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.2) !important;
    }

    /* File uploader style override */
    .stFileUploader section {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(79, 172, 254, 0.3) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }

    .stFileUploader section:hover {
        border-color: #00f2fe !important;
        background-color: rgba(0, 242, 254, 0.02) !important;
    }

    /* Answer box */
    .answer-box {
        background: rgba(0, 242, 254, 0.03);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        color: #f3f4f6;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Main Application Title
st.markdown("<h1>📄 PDF Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask questions based strictly on your uploaded document context</p>", unsafe_allow_html=True)

# Initialize vector store session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = load_vector_store()

# PDF Processing Section
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("1. Upload and Process PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

process_btn = st.button("Process PDF")

if process_btn:
    if uploaded_file is not None:
        with st.spinner("Analyzing PDF and generating vector database..."):
            # Save file temporarily to disk to be read by PyPDFLoader
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Process PDF and build local FAISS store
                st.session_state.vector_store = process_pdf(tmp_file_path)
                st.success(f"Success! '{uploaded_file.name}' has been successfully processed and indexed.")
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
            finally:
                # Ensure temporary file is cleaned up
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
    else:
        st.warning("Please upload a PDF file first before clicking Process.")
st.markdown("</div>", unsafe_allow_html=True)

# Q&A Section
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("2. Ask Your Question")
question = st.text_input("Enter your question:", placeholder="What does the document say about...")

ask_btn = st.button("Ask")

if ask_btn:
    if not st.session_state.vector_store:
        st.warning("No processed PDF found. Please upload a PDF and click 'Process PDF' first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching document and generating response..."):
            try:
                # Query the pipeline to get response
                answer = get_answer(question, st.session_state.vector_store)
                st.markdown("### Answer:")
                st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
st.markdown("</div>", unsafe_allow_html=True)
