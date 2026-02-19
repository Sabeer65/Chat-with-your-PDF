# Chat with your PDF using Retrieval-Augmented Generation (RAG)

This repository contains a locally running document question-answering system that allows users to interact with PDF files using natural language queries. The system uses a Retrieval-Augmented Generation (RAG) approach to provide answers grounded strictly in the uploaded document content.

The entire pipeline runs locally without external API calls or cloud services.

## Project Overview

Reading and searching through long PDF documents can be inefficient. This project simplifies that process by enabling users to:

- Load a PDF document
- Ask questions in natural language
- Receive answers based only on the document’s content

The system works by extracting text from the PDF, splitting it into smaller chunks, converting those chunks into vector embeddings, and storing them in a local FAISS vector database. When a question is asked, relevant text segments are retrieved and used to generate a context-aware response.

### Key Features

- **PDF Text Extraction:** Extracts text directly from PDF files.
- **Text Chunking:** Breaks large documents into manageable searchable sections.
- **Local Vector Search (FAISS):** Enables semantic retrieval without external services.
- **Context-Grounded Responses:** Answers are generated strictly from retrieved document content.
- **Fully Local Execution:** No external APIs, cloud models, or hosted services required.
- **Docker Support:** Containerized setup available for consistent local deployment.

## Repository Structure

- `app.py` – Contains the main RAG pipeline implementation.
- `requirements.txt` – Lists required Python libraries.
- `Dockerfile` – Defines the containerized environment.
- `docker-compose.yml` – Optional multi-container setup configuration.
- `README.md` – Project documentation.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Sabeer65/Chat-with-your-PDF.git
cd Chat-with-your-PDF
pip install -r requirements.txt
```

## Docker Setup

You can also run the application using Docker.

Build the Docker image:

```bash
docker build -t chat-with-your-pdf .
```

Run the container:

```bash
docker run -p 8501:8501 chat-with-your-pdf
```

Then open your browser and navigate to:

http://localhost:8501

If using Docker Compose:

```bash
docker-compose up --build
```

## Usage

Run the application locally:

```bash
streamlit run app.py
```

Steps:

1. Load a PDF file.
2. Enter a question related to the document.
3. The system retrieves relevant sections and generates an answer.

## How It Works

1. The PDF is loaded and text is extracted.
2. The text is divided into smaller chunks.
3. Each chunk is converted into embeddings.
4. Embeddings are stored in a local FAISS vector store.
5. A user query is embedded and matched against stored vectors.
6. The most relevant chunks are used to generate a response.

## Limitations

- Scanned PDFs without readable text may not work properly.
- Very large documents may increase indexing time.
- Accuracy depends on chunking strategy and embedding quality.

## Learning Outcomes

This project demonstrates:

- Practical implementation of a RAG pipeline
- Vector similarity search using FAISS
- Building document-based QA systems
- Handling real-world unstructured data
