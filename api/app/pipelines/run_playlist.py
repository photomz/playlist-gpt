from pathlib import Path
import sys

# Move import to root directory
sys.path.insert(0, str(Path(__file__).parents[2].resolve()))

import dotenv
dotenv.load_dotenv()

import os, webbrowser, time
from app.services.spotify import get_spotify_access_token, delete_spotify_playlist
from app.api.playlist import generate_playlist
from app.api.spotify import spotify

def main():
    default = 'Velvety princess pop in a cafe'
    text = input(f"Prompt (default='{default}'): ") or default

    start = time.time()
    # create a chat completion
    result = generate_playlist(text)

    spotify_playlist = spotify(os.getenv('SPOTIFY_HARDCODE_TOKEN'), os.getenv('SPOTIFY_HARDCODE_ID'), result) # type: ignore

    webbrowser.open(spotify_playlist.url)

    end = time.time()
    print(f"Time elapsed: {end-start} seconds")

    input("Hit [Enter] to delete.")

    delete_spotify_playlist(spotify_playlist.spotify_id, os.getenv('SPOTIFY_HARDCODE_TOKEN'))

if __name__ == '__main__':
    main()
