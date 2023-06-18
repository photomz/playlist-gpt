from dataclasses import dataclass, field
from app.services.spotify import create_spotify_playlist, Playlist

# SpotifyPlaylist dataclass with spotify id, id, username, url
@dataclass
class SpotifyPlaylist:
    """Response from created Spotify playlist object"""
    id: str
    spotify_id: str
    username: str
    url: str

def spotify(user_token: str, username: str, playlist: Playlist):
    title = playlist.title
    description = playlist.description
    image = playlist.image_url
    songs = playlist.songs
    # TODO: Get playlist from db given id

    song_ids = (song.id for song in songs)
    playlist_url, spotify_playlist_id = create_spotify_playlist(
        title=title,
        description=f"{description} (made by playlist-gpt)",
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