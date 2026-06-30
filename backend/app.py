# FastAPI entrypoint. Run with:  uvicorn app:app --reload  (from the backend/ dir)

import os
import sys

# Ensure this backend/ dir is on sys.path so the BiasAI / BiasRuleAlgo packages
# import regardless of the working directory. Needed on Vercel, where the
# entrypoint is backend/app.py but only the task root is on sys.path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from BiasAI.controller import router as bias_router

app = FastAPI(title="University CV Bias Toolkit")

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
