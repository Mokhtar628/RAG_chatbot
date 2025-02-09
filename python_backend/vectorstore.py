"""
vectorstore.py

This script processes text documents from a specified directory, converts them into vector embeddings,  
and stores them in a FAISS (Facebook AI Similarity Search) index for efficient retrieval.  

Functionality:
1. **Load Documents**: Reads all `.txt` files from the `data` directory and converts them into LangChain `Document` objects.  
2. **Text Splitting**: Uses `RecursiveCharacterTextSplitter` to divide documents into smaller overlapping chunks  
   to improve retrieval performance.  
3. **Embedding Generation**: Uses the `HuggingFaceEmbeddings` model (`all-mpnet-base-v2`) to create vector representations  
   of document chunks.  
4. **FAISS Indexing**: Builds a FAISS-based vector store to enable fast similarity search.  
5. **Execution**: When run as a standalone script, it prints the number of document chunks stored in the FAISS index.  

This script is useful for building a local knowledge base for retrieval-augmented generation (RAG) tasks  
or for implementing a document search system using embeddings.
"""

import os
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_documents(data_dir="data"):
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text, metadata={"source": filename}))
    return documents

def build_vectorstore(data_dir="data"):
    documents = load_documents(data_dir)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

if __name__ == "__main__":
    vs = build_vectorstore()
    print(f"Vectorstore built with {len(vs.index_to_doc)} document chunks.")
