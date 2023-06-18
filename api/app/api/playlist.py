import openai, os, yaml, random
from typing import Optional
from dataclasses import asdict
from fastapi import APIRouter
from pydantic import BaseModel
from app.helpers.prompt import format
from app.services.unsplash import batch_search_unsplash
from app.services.spotify import get_spotify_access_token, batch_search_spotify
from app.helpers.types import Playlist
from app.services.db import table

# TODO: Token resets every hour. Remember to refresh in cron job?
spotify_token = get_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET')) # type: ignore

def generate_playlist(prompt, spotify_token=spotify_token):
    formatted = format(prompt)
    raw_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": formatted}],
        stop=['```'],
        temperature=0.7
    )

    # print the chat completion
    completion = raw_completion.choices[0].message.content # type: ignore
    print(completion)

    yaml_completion = yaml.safe_load(completion)
    print(yaml_completion)

    image_url = random.choice(batch_search_unsplash([yaml_completion['image']], [5])[0])
    print(image_url)

    # [{title, artist}] -> [titles], [artists]
    titles = [key for _dict in yaml_completion['tracks'] for key in _dict.keys()]
    artists = [value for _dict in yaml_completion['tracks'] for value in _dict.values()]

    songs = batch_search_spotify(titles, artists, spotify_token) # type: ignore
    song_ids = [song.id for song in songs if song]
    print(song_ids)

    playlist = Playlist(
        title=yaml_completion['title'],
        description=yaml_completion['description'] + ' (made by playlist-gpt)',
        image_url=image_url,
        prompt=prompt,
        audio_url='', # TODO: generate 3sec clips per song
        model_result=completion,
        songs=songs
    )
    id = table.insert(asdict(playlist))
    playlist.id = id

    return playlist

router = APIRouter()
class DesignBody(BaseModel):
    prompt: str
    request_id: Optional[str]


@router.post("/")
def design(body: DesignBody):
    return generate_playlist(body.prompt)