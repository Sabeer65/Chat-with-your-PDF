from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

def process_pdf(pdf_file, ollama_base_url):
    reader = PdfReader(pdf_file)
    pdf_text = ''

    for pages in reader.pages:
        pdf_text += pages.extract_text()
    
    # Splitting the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=0)
    chunks = text_splitter.split_text(pdf_text)

    # embedding the text and storing it in session state
    embeddings = OllamaEmbeddings(model="llama3.2", base_url=ollama_base_url)
    
    vector_store = FAISS.from_texts(chunks, embeddings)

    return vector_store