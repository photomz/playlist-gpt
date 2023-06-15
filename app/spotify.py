import requests
from requests.auth import HTTPBasicAuth
import asyncio
from typing import List
from arequests import fetch_all

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
    
def batch_search_spotify(song_names: List[str], access_token: str) -> List[str | None]:
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
                song_ids.append(search_results["tracks"]["items"][0]["id"])
            else:
                # Silent fallback
                song_ids.append(None)

        return song_ids
    except Exception as e:
        print(f"Error in Spotify: {e}")
        # Silent fallback: append None
        # This assumes that the caller handles None appropriately
        return [None] * len(song_names)

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
        song_ids = batch_search_spotify(song_names, access_token)
        print(song_ids)
        end = time.time()
        print(f"Time elapsed: {end-start} seconds")