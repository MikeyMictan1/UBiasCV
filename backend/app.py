# FastAPI entrypoint. Run with:  uvicorn app:app --reload  (from the backend/ dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from BiasAI.controller import router as bias_router

app = FastAPI(title="University Admissions Bias Toolkit")

# Open CORS for the prototype (Vite dev server, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bias_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
