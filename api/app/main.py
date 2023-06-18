import os, dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

from app.api import playlist

app = FastAPI()

# Configure CORS
origins = [
		"http://localhost",
		"http://localhost:8080",
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

print(f"API Server Active on {os.getenv('ENV')} 🚀")
