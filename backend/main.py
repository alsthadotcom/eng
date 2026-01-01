from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_full_word_data
import os
import uvicorn

app = FastAPI()

# Allow CORS for all origins for deployment ease
origins = ["*"]

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
