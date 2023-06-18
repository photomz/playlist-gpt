from pathlib import Path
import sys

# Move import to root directory
sys.path.insert(0, str(Path(__file__).parents[2].resolve()))

import dotenv
dotenv.load_dotenv()

import os, webbrowser, time
from app.helpers.prompt import format
from app.services.spotify import get_spotify_access_token, delete_spotify_playlist
from app.api.playlist import playlist
from app.api.spotify import spotify

def main():
    # TODO: Token resets every hour. Remember to refresh in cron job?
    spotify_token = get_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET')) # type: ignore
    
    default = 'Motivational run at sunset'
    text = input(f"Prompt (default='{default}'): ") or default

    start = time.time()
    # create a chat completion
    result = playlist(spotify_token, text)

    spotify_playlist = spotify(os.getenv('SPOTIFY_HARDCODE_TOKEN'), os.getenv('SPOTIFY_HARDCODE_ID'), result) # type: ignore

    webbrowser.open(spotify_playlist.url)

    end = time.time()
    print(f"Time elapsed: {end-start} seconds")

    input("Hit [Enter] to delete.")

    delete_spotify_playlist(spotify_playlist.spotify_id, os.getenv('SPOTIFY_HARDCODE_TOKEN'))

if __name__ == '__main__':
    main()
