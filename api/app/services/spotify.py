from dataclasses import dataclass, field
from typing import List
import requests
from requests.auth import HTTPBasicAuth
import asyncio
from typing import List, Optional
from app.helpers.arequests import fetch_all
import json
from app.helpers.image import get_base64_encoded_image
from urllib.parse import quote_plus

# Song dataclass with id, name, artist, album, year, duration_ms, audio_url
@dataclass
class Song:
    """Spotify song dataclass"""
    id: str # Spotify ID
    name: str
    artist: str
    album: str
    year: int
    duration_ms: int
    image_url: str # Album image url
    audio_url: Optional[str] = None # Spotify audio URL, not available for all songs

# Playlist dataclass with title, description, image, prompt, id, audio url, a list of songs
@dataclass
class Playlist:
    """Spotify playlist dataclass"""
    id: str
    title: str
    description: str
    image_url: str
    prompt: str
    audio_url: str
    songs: List[Song] = field(default_factory=list)
    
def get_spotify_access_token(client_id: str, client_secret: str) -> str | None:
    """
    Retrieves a Spotify access token using the OAuth2 server-side flow.

    Args:
        client_id (str): The client ID obtained from the Spotify Developer Dashboard.
        client_secret (str): The client secret obtained from the Spotify Developer Dashboard.

    Returns:
        str: The access token if successfully retrieved, None otherwise.
    """
    
    # Set up the authentication parameters
    auth_url = 'https://accounts.spotify.com/api/token'
    auth = HTTPBasicAuth(client_id, client_secret)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Prepare the request payload
    data = {
        'grant_type': 'client_credentials'
    }

    # Send the POST request to retrieve the access token
    response = requests.post(auth_url, auth=auth, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("Failed to retrieve Spotify access token.")
        return None
    
def find_key(key: str, data: list, target: str) -> int:
    """Find index where key matches target value in a list of dictionaries."""
    if not data:
        raise ValueError("Data is empty.")
    for i,item in enumerate(data):
        if item.get(key) == target:
            return i
    return 0
    
def batch_search_spotify(titles: List[str], artists: List[str], access_token: str) -> List[Song]:
    """Batch search song ids on Spotify with the Spotify API and asyncio.

    Args:
        song_names (List[str]): List of song names.
        access_token (str): Spotify access token.

    Returns:
        List[dict]: List of song ids
    """
    song_names = [f"{title} by {artist}" for title, artist in zip(titles, artists)]
    # Headers for Spotify API requests
    headers = [{
        "Authorization": f"Bearer {access_token}"
    }]*len(song_names)

    # Spotify's search API endpoint
    base_urls = [f"https://api.spotify.com/v1/search?q={quote_plus(song_name)}&type=track&limit=10&offset=0" for song_name in song_names]

    print(base_urls)

    try:
        # Fetch the song ids
        batch_responses = asyncio.run(
            fetch_all(base_urls, headers=headers)
        )

        song_ids = []
        for search_results, artist in zip(batch_responses, artists):
            if search_results and "tracks" in search_results and "items" in search_results["tracks"] and len(search_results["tracks"]["items"]) > 0:
                tracks = search_results['tracks']['items']

                track = None
                for item in tracks:
                    # Check if the artist name of the current item matches the target artist
                    if item['artists'][0]['name'] == artist:
                        # If a match is found, assign the current item to the `track` variable
                        track = item
                        break
                else:
                    # If no match is found, assign the first item in `tracks` to the `track` variable
                    track = tracks[0]


                track_info = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'year': track['album']['release_date'][:4],
                    'duration_ms': track['duration_ms'],
                    'image_url': track['album']['images'][0]['url'],
                    'audio_url': track['preview_url']
                }

                song_ids.append(Song(**track_info))

                # Get "name, artist" string for each track
                available_tracks = [f"{track['name']}, {track['artists'][0]['name']}" for track in search_results['tracks']['items']]
                print(available_tracks)

                print(track['artists'][0]['name'])
            else:
                # Silent fallback
                pass
                # song_ids.append(None)

        return song_ids
    except Exception as e:
        print(f"Error in Spotify: {e}")
        # Silent fallback: append None
        # This assumes that the caller handles None appropriately
        return [] # [None] * len(song_names)
    
def add_tracks_to_playlist(playlist_id, track_ids, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'uris': ['spotify:track:' + track_id for track_id in track_ids],
    }

    response = requests.post(
        f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
        headers=headers,
        data=json.dumps(payload),
    )

    if response.status_code != 201:
        print("Failed to add tracks to the playlist.")

def set_playlist_cover_image(playlist_id, image_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'image/jpeg',
    }

    base64_encoded_image = get_base64_encoded_image(image_url)

    response = requests.put(
        f'https://api.spotify.com/v1/playlists/{playlist_id}/images',
        headers=headers,
        data=base64_encoded_image,
    )
    
    if response.status_code != 202:
        print("Failed to set the playlist cover image.")
        

def create_spotify_playlist(title, description, track_ids, image_url, access_token, user_id):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'name': title,
        'description': description,
        'public': True,
        'collaborative': False,
    }

    response = requests.post(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers=headers,
        data=json.dumps(payload),
    )

    if response.status_code == 201:
        playlist_id = response.json()['id']
        add_tracks_to_playlist(playlist_id, track_ids, access_token)
        set_playlist_cover_image(playlist_id, image_url, access_token)

        playlist_url = response.json()['external_urls']['spotify']
        return playlist_url, playlist_id
    elif response.status_code == 401:
        # Raise Auth error
        raise Exception(f"Failed to create the playlist. The access token is invalid:\n{response.json()}")
    else:
        return None, None

def delete_spotify_playlist(playlist_id, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.delete(
        f'https://api.spotify.com/v1/playlists/{playlist_id}/followers',
        headers=headers,
    )

    if response.status_code == 200:
        return True
    else:
        print(f"Failed to delete the playlist with ID {playlist_id}.")
        print(response)
        return False

# Example usage
if __name__ == '__main__':
    import dotenv, os, time
    dotenv.load_dotenv()
        
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    access_token = get_spotify_access_token(client_id, client_secret) # type: ignore
    if access_token:
        print("Access token:", access_token)

        start = time.time()
        song_names = ["Shake it Off", "Blank Space", "Bad Blood", "Wildest Dreams", "Look What You Made Me Do"]
        artists = ["Taylor Swift"] * len(song_names)
        songs = batch_search_spotify(song_names, artists, access_token)
        print(songs)
        end = time.time()
        print(f"Time elapsed: {end-start} seconds")

        # Create playlist given ids, with random title+description+image

        TOKEN = os.getenv('SPOTIFY_HARDCODE_TOKEN')
        ID = os.getenv('SPOTIFY_HARDCODE_ID')

        song_ids  = [song.id for song in songs if song]
        # Now time in readable format
        from datetime import datetime
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        playlist_id = create_spotify_playlist(
            title="Swifty Playlist",
            description=f"For your dear Swifties at {now} (made by playlist-gpt)",
            track_ids=song_ids,
            image_url="https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzODczMzh8MHwxfHNlYXJjaHwxfHxmaXNofGVufDF8fHx8MTY4Njg2OTI4M3ww&ixlib=rb-4.0.3&q=80&w=400",
            access_token=TOKEN,
            user_id=ID,
        )