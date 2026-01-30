import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
import time

st.title("Chat with your PDF")

llm = ChatOllama(model="llama3.2", temperature=0)

pdffile = st.file_uploader(label="Upload your pdf", accept_multiple_files=False, type=["pdf"])

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


if pdffile is not None:
    try:
        
        # checking if already processed to save time 
        if st.session_state.vector_store is None:

            reader = PdfReader(pdffile)
            pdf_text = ''

            with st.spinner("Wait for it...", show_time=True):
                for pages in reader.pages:
                    pdf_text += pages.extract_text()

                # Splitting the text into chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                chunks = text_splitter.split_text(pdf_text)
                
                # embedding the text and storing it in session state
                embeddings = OllamaEmbeddings(model="llama3.2")
                st.session_state.vector_store = FAISS.from_texts(chunks, embeddings)

            st.success("Pdf Loaded succesfully")


    except Exception as exc:
        st.error(f"Failed to load PDF {exc}")

    user_input = st.chat_input("Type your question here")

    # If no user input or vector_store do not run code
    if user_input and st.session_state.vector_store is not None:

        st.chat_message("user").write(user_input)
        
        with st.spinner("Thinking..."):
            # Search for the user input in the vector store
            docs = st.session_state.vector_store.similarity_search(user_input)

            if docs:
                context = ''
                for doc in docs:
                    context += doc.page_content +"\n\n" # Set the context from the docs
                
                # Prompt for the llm 
                prompt = f"""
            You are a helpful AI assistant. 
            The user has uploaded a PDF document, and here is the relevant content extracted from it:
            
            --- PDF CONTENT START ---
            {context}
            --- PDF CONTENT END ---
            
            User Question: {user_input}
            
            Answer (based ONLY on the PDF content above):
            """
                
                response = llm.invoke(prompt)
                st.chat_message("assistant").write(response.content)

            else:
                st.warning("i couldnt find any relevant info in the PDF")