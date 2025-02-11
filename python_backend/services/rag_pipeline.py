# This script sets up a question-answering system using LangChain, Hugging Face's Flan-T5-large model, and a custom vectorstore.
# It retrieves relevant context from the vectorstore based on a user's question and uses the LLM to generate a concise and informative answer.
# It also handles greetings and cases where no relevant information is found.
# running dirctly will allow you to test the service from the cmd


from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from services.vectorstore import get_vectorstore
import torch


vectorstore = get_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


def create_hf_pipeline():
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    #print(tokenizer.model_max_length)

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

    if not context.strip():
        return "I'm sorry, I couldn't find that information."

    max_length = 600
    if len(context) > max_length:
        context = context[:max_length]

    
    prompt = f"""
        You are an AI assistant for XYZ Company, developed by Mokhtar.

        If answering policy-related questions, ensure consistency with past responses.

        If the answer is not explicitly stated but can be inferred from context, provide the best possible answer.
        If no relevant information is available, respond with: "I'm sorry, I couldn't find that information."

        Context: {context}

        Question: {question}

        Provide a clear, professional, consistent, user-friendly, and concise answer based on the above context.
    """


    result = qa_chain.invoke({"query": prompt})
    return result["result"]

# if __name__ == "__main__":
    print("\n🤖 RAG Chatbot is running tests...\n")
    
    test_questions = [
    # Leave Policies
    "What is your leave policy?",
    "Can you tell me more about your leave policy?",
    "Could you explain the leave policy in detail?",
    "How many days of annual leave do employees get?",
    "Is sick leave paid or unpaid?",
    "What is the procedure to apply for sick leave?",
    "How long is maternity leave?",
    "Do you offer paternity leave?",
    "Which public holidays do employees get off?",
    
    # Working Hours & Attendance
    "What are the working hours?",
    "Do you offer flexible working hours?",
    "Are employees allowed to work remotely?",
    "What happens if I’m late to work?",
    "What is the lunch break policy?",
    "Do you allow half-day leaves?",
    
    # Compensation & Benefits
    "When do employees get paid?",
    "Do you provide health insurance?",
    "Can employees extend health insurance to family members?",
    "How are performance bonuses determined?",
    "Is there a probation period for new employees?",
    
    # Workplace Conduct & Disciplinary Actions
    "What disciplinary actions can XYZ Company take for policy violations?",
    "What behaviors are considered misconduct?",
    "How do I report harassment?",
    "What should I do if I have an ethical concern?",
    "What is the code of conduct at XYZ Company?",
    
    # Overtime & Extra Work
    "How is overtime compensated?",
    "Do employees get paid for working extra hours?",
    "Can I work overtime without prior approval?",
    "Is there a limit to how much overtime I can do?",
    
    # Termination & Resignation
    "What are the reasons an employee can be terminated?",
    "What is the notice period for resignation?",
    "How soon will I receive my final settlement after resignation?",
    "Do you conduct exit interviews?",
    
    # Confidentiality & Data Protection
    "What is XYZ Company’s confidentiality policy?",
    "Are employees required to sign an NDA?",
    "How does XYZ Company protect employee data?",
    
    # Miscellaneous
    "How often does XYZ Company update its HR policy?",
    "Where can I find the latest HR policy updates?",
    "What happens if an employee violates the confidentiality agreement?",
]

    
    for idx, question in enumerate(test_questions, 1):
        print(f"You ({idx}): {question}")
        response = get_answer(question)
        print(f"Bot: {response}\n")
    
    print("Testing completed. Enter 'exit' to quit or ask your own questions.\n")
    
    while True:
        user_question = input("You: ").strip()
        
        if user_question.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        response = get_answer(user_question)
        print(f"Bot: {response}\n")



if __name__ == "__main__":
    print("\n🤖 RAG Chatbot is ready! Type 'exit' to quit.\n")
    
    while True:
        user_question = input("You: ").strip()
        
        if user_question.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        response = get_answer(user_question)
        print(f"Bot: {response}\n")


"""
    Answer the question **ONLY based on the provided company policy document**.
        Do not make up information. If the answer is not explicitly stated, respond with "I'm sorry, I couldn't find that information."

    """