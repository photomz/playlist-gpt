import os, dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

from app.api import playlist, spotify, db, semantic_search

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
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
async def health():
    return {"status": "ok"}


app.include_router(
    playlist.router,
    prefix="/playlist",
)

app.include_router(
    spotify.router,
    prefix="/spotify",
)

app.include_router(
    db.router,
    prefix="/db",
)

app.include_router(
    semantic_search.router,
    prefix="/search",
)

print(f"API Server Active on {os.getenv('ENV')} 🚀")
