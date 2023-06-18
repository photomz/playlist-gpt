from app.services.spotify import create_spotify_playlist
from fastapi import APIRouter
from pydantic import BaseModel
from app.helpers.types import SpotifyPlaylist, Playlist
from app.services.db import table

def spotify(user_token: str, username: str, id: int):
    playlist = table.get(doc_id=id)
    
    if not playlist:
        raise Exception('Playlist not found')
    print(playlist)
    playlist = Playlist(**playlist) # type: ignore
    
    title = playlist.title
    description = playlist.description
    image = playlist.image_url
    songs = playlist.songs
    # TODO: Get playlist from db given id

    song_ids = (song['id'] for song in songs) # type: ignore
    playlist_url, spotify_playlist_id = create_spotify_playlist(
        title=title,
        description=description,
        track_ids=song_ids,
        image_url=image,
        access_token=user_token, #os.getenv('SPOTIFY_HARDCODE_TOKEN'),
        user_id=username #os.getenv('SPOTIFY_HARDCODE_ID')
    )
    uploaded_playlist = SpotifyPlaylist(
        id=playlist.id,
        spotify_id=spotify_playlist_id, # type: ignore
        username=username,
        url=playlist_url # type: ignore
    )
    return uploaded_playlist

router = APIRouter()
class DesignBody(BaseModel):
    user_token: str
    username: str
    id: int

@router.post("/")
def design(body: DesignBody):
    return spotify(body.user_token, body.username, body.id)

