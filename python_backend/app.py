# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import get_answer

app = FastAPI(title="RAG Chatbot Backend")

# Define the expected request body using Pydantic.
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    """
    Receives a JSON payload with a 'question' field, processes it using the RAG pipeline,
    and returns the generated answer.
    """
    try:
        answer = get_answer(query.question)
        return {"question": query.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the FastAPI app using uvicorn when this module is executed directly.
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
