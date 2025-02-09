"""
rag_chatbot.py

This script implements a Retrieval-Augmented Generation (RAG) chatbot using LangChain, Hugging Face Transformers,  
and FAISS for efficient document retrieval and response generation.

Functionality:
1. **Vectorstore Construction**: 
   - Loads text documents from the `data` directory.
   - Converts them into vector embeddings using a Hugging Face model.
   - Stores the embeddings in a FAISS index for quick similarity search.

2. **Retriever Setup**: 
   - Retrieves the most relevant document chunks (`k=2`) for a given user query.

3. **Hugging Face Text Generation Pipeline**:
   - Loads a `FLAN-T5` model for text generation.
   - Uses `bfloat16` precision and `device_map="cuda"` for optimized performance.
   - Applies sampling techniques (`temperature=0.7`, `top_p=0.85`, `repetition_penalty=1.1`)  
     to balance response diversity and relevance.

4. **RetrievalQA Chain**:
   - Uses LangChain's `RetrievalQA` to answer queries based on retrieved document content.
   - Ensures responses are strictly based on company policy documents.
   - Limits answer length and enforces consistency in responses.

5. **Interactive Chatbot**:
   - Provides a CLI-based chatbot experience.
   - Handles common greetings and unknown queries gracefully.
   - Runs an interactive loop where users can ask questions and receive AI-generated responses.

This script is ideal for building AI-powered customer support, knowledge base assistants,  
or policy document Q&A systems.
"""

from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from vectorstore import build_vectorstore
import torch


# --- Build the vectorstore and retriever ---
vectorstore = build_vectorstore(data_dir="data")
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


def create_hf_pipeline():
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name, 
        torch_dtype=torch.bfloat16,
        device_map="cuda" 
    )

    hf_pipeline = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_p=0.85,
        repetition_penalty=1.1
    )
    return hf_pipeline


hf_pipeline = create_hf_pipeline()
llm = HuggingFacePipeline(pipeline=hf_pipeline)

qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)


def get_answer(question: str) -> str:    
    greetings = [
        "hello", "hi", "hey", "howdy", "hola", "greetings", "sup", "yo",
        "good morning", "morning", "good afternoon", "afternoon",
        "good evening", "evening", "good day", "what's up", "wassup",
        "how's it going", "how are you", "how have you been",
        "nice to meet you", "pleased to meet you"
    ]
    if question.lower() in greetings:
        return "Hello! I am an AI assistant for XYZ Company, developed by Mokhtar. How can I assist you today?"

    relevant_docs = retriever.invoke(question)

    context = " ".join([doc.page_content for doc in relevant_docs])

    # print(f"context is {context}")

    if not context.strip():
        return "I'm sorry, I couldn't find that information."

    max_length = 512
    if len(context) > max_length:
        context = context[:max_length]

    prompt = f"""
        You are an AI assistant for XYZ Company, developed by Mokhtar.

        Answer the question **ONLY based on the provided company policy document**.
        Do not make up information. If the answer is not explicitly stated, respond with "I'm sorry, I couldn't find that information."

        If answering policy-related questions, ensure consistency with past responses.
        
        **Context:** {context}

        **Question:** {question}

        Provide a **clear, professional, consistent, user-friendly and concise answer** based on the above context.
    """

    result = qa_chain.invoke({"query": prompt})
    return result["result"]




if __name__ == "__main__":
    print("\n🤖 RAG Chatbot is ready! Type 'exit' to quit.\n")
    
    while True:
        user_question = input("You: ").strip()
        
        if user_question.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        response = get_answer(user_question)
        print(f"Bot: {response}\n")
