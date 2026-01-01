from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_full_word_data
import os
import uvicorn

# Allow CORS for React Frontend (usually runs on port 5173 or 3000)
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "English Learning API is running"}

@app.get("/api/random-word")
def get_random_word():
    """Fetches a random word and all related data."""
    data = get_full_word_data()
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
