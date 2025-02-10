"""
vectorstore.py

This script creates and manages a FAISS vector store for efficient document retrieval.
It loads text documents from the 'data' directory, splits them into chunks, generates embeddings using a Hugging Face model (all-mpnet-base-v2), and stores them in the FAISS index.
This allows for fast similarity searches when answering questions based on the document content.  
Running the script directly will print the number of stored document chunks.

Here are some resources:
- https://huggingface.co/sentence-transformers/all-mpnet-base-v2
- here are a comparison between some state-of-the-art sentence transeformares https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
- here is a comparison between different vector_store models: https://python.langchain.com/docs/integrations/vectorstores/
- here are the top 7 vector databases for 2025 according to datacamp: https://www.datacamp.com/blog/the-top-5-vector-databases
"""

import os
import pickle
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_documents(data_dir="../data"):
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text, metadata={"source": filename}))
    return documents

def build_vectorstore(data_dir="../data"):
    documents = load_documents(data_dir)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def get_vectorstore(store_path="../vector_database/vectorstore.pkl", data_dir="../data"):
    if os.path.exists(store_path):
        print("Loading saved vector store...")
        with open(store_path, "rb") as f:
            vectorstore = pickle.load(f)
    else:
        print("No saved vector store found. Building vector store...")
        vectorstore = build_vectorstore(data_dir)
        with open(store_path, "wb") as f:
            pickle.dump(vectorstore, f)
    return vectorstore

if __name__ == "__main__":
    vs = get_vectorstore()
    print(f"Vectorstore loaded with {len(vs.index_to_doc)} document chunks.")
