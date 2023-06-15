from dataclasses import dataclass
import requests
from requests.auth import HTTPBasicAuth
import asyncio
from typing import List
from arequests import fetch_all
import json
from image import get_base64_encoded_image

# Create a dataclass from track_info
@dataclass
class TrackInfo:
    """Dataclass for track information."""
    id: str
    name: str
    artist: str
    duration: int
    image_url: str

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
    
def batch_search_spotify(song_names: List[str], access_token: str) -> List[TrackInfo | None]:
    """Batch search song ids on Spotify with the Spotify API and asyncio.

    Args:
        song_names (List[str]): List of song names.
        access_token (str): Spotify access token.

    Returns:
        List[dict]: List of song ids
    """
    # Headers for Spotify API requests
    headers = [{
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }]*len(song_names)

    # Spotify's search API endpoint
    base_urls = [f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1" for song_name in song_names]

    try:
        # Fetch the song ids
        batch_responses = asyncio.run(
            fetch_all(base_urls, headers=headers)
        )

        song_ids = []
        for search_results in batch_responses:
            if search_results and "tracks" in search_results and "items" in search_results["tracks"] and len(search_results["tracks"]["items"]) > 0:
                track = search_results['tracks']['items'][0]
                track_id = track['id']
                track_name = track['name']
                artist = track['artists'][0]['name']
                duration_ms = track['duration_ms']
                cover_image_url = track['album']['images'][0]['url']

                track_info = TrackInfo(track_id, track_name, artist, duration_ms, cover_image_url)
                song_ids.append(track_info)
            else:
                # Silent fallback
                song_ids.append(None)

        return song_ids
    except Exception as e:
        print(f"Error in Spotify: {e}")
        # Silent fallback: append None
        # This assumes that the caller handles None appropriately
        return [None] * len(song_names)
    
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
        return playlist_url
    else:
        return None

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
        songs = batch_search_spotify(song_names, access_token)
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