import streamlit as st
from langchain_ollama import ChatOllama
import os 
from utils import process_pdf, format_chat_history

st.title("Chat with your PDF")

ollama_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

llm = ChatOllama(model="llama3.2",base_url=ollama_base_url, temperature=0)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

with st.sidebar:

    pdffile = st.file_uploader(label="Upload your pdf", accept_multiple_files=False, type=["pdf"])
    
    if pdffile is not None:
        if st.session_state.vector_store is None:
            try:
                with st.spinner("Wait for it...", show_time=True):
                    st.session_state.vector_store = process_pdf(pdffile, ollama_base_url)
                st.success("Pdf Loaded succesfully")

            except Exception as exc:
                st.error(f"Failed to load PDF {exc}")

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

user_input = st.chat_input("Type your question here")

# If no user input or vector_store do not run code
if user_input and st.session_state.vector_store is not None:

    history = format_chat_history(st.session_state.messages)
    
    st.session_state.messages.append({'role':'user', 'content':user_input})

    with st.chat_message("user"):
        st.write(user_input)

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

        --- CHAT HISTORY ---
            {history}
            --------------------

        The user has uploaded a PDF document, and here is the relevant content extracted from it:
        
        --- PDF CONTENT START ---
        {context}
        --- PDF CONTENT END ---
        
        User Question: {user_input}
        
        Answer (based ONLY on the PDF content above):
        """
            
            response = llm.invoke(prompt)

            st.session_state.messages.append({'role':'assistant', 'content':response.content})

            with st.chat_message("assistant"):
                st.write(response.content)

        else:
            st.warning("i couldnt find any relevant info in the PDF")