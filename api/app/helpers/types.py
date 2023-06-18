from dataclasses import dataclass, field
from typing import List, Optional

# SpotifyPlaylist dataclass with spotify id, id, username, url
@dataclass
class SpotifyPlaylist:
    """Response from created Spotify playlist object"""
    spotify_id: str
    username: str
    url: str
    id: Optional[int] = None # Playlist id

# Song dataclass with id, name, artist, album, year, duration_ms, audio_url
@dataclass
class Song:
    """Spotify song dataclass"""
    id: str # Spotify ID
    name: str
    artist: str
    album: str
    year: str
    url: str # Spotify track URL
    album_id: str
    track_num: int # Track number in album
    duration_ms: int
    image_url: str # Album image url
    audio_url: Optional[str] = None # Spotify audio URL, not available for all songs

# Playlist dataclass with title, description, image, prompt, id, audio url, a list of songs
@dataclass
class Playlist:
    """Spotify playlist dataclass"""
    title: str
    description: str
    image_url: str
    prompt: str
    audio_url: str
    model_result: str # Raw ChatGPT model result
    songs: List[Song] = field(default_factory=list)
    id: Optional[int] = None # Empty until saved to db