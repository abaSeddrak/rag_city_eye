from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_chain import ask
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="City Eye RAG API",
    description="API للإجابة عن أسئلة قواعد City Eye",
    version="1.0"
)

# CORS للسماح بالـ requests من أي مكان
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list

@app.get("/")
def root():
    return {
        "message": "City Eye RAG API",
        "endpoints": {
            "POST /query": "اسأل سؤال",
            "GET /health": "فحص الحالة"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="السؤال فارغ")
        
        answer, docs = ask(request.question)
        
        sources = [
            {
                "page": doc.metadata.get("page", "?"),
                "content": doc.page_content[:200]
            }
            for doc in docs
        ]
        
        return {
            "question": request.question,
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)