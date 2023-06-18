import numpy as np
import openai
from fastapi import APIRouter
from pydantic import BaseModel

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def cosine_similarity(embedding1, embedding2):
    norm_embedding1 = np.linalg.norm(embedding1)
    norm_embedding2 = np.linalg.norm(embedding2)

    # Check for zero division
    if norm_embedding1 == 0 or norm_embedding2 == 0:
        return 0.0

    dot_product = np.dot(embedding1, embedding2)
    similarity = dot_product / (norm_embedding1 * norm_embedding2)
    return similarity



def semantic_search(prompt):
    prompt_embedding = get_embedding(prompt)
    playlist_embeddings = np.load('bin/playlist.npy')

    similarities = [cosine_similarity(prompt_embedding, playlist_embedding) for playlist_embedding in playlist_embeddings]
    similarities = list(enumerate(similarities))

    similarities.sort(reverse=True, key=lambda x: x[1])

    return similarities


router = APIRouter()
class DesignBody(BaseModel):
    prompt: str

@router.post("/search")
def design(body: DesignBody):
    return semantic_search(body.prompt)