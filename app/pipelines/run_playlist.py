from pathlib import Path
import sys

# Move import to root directory
sys.path.insert(0, str(Path(__file__).parents[2].resolve()))

import dotenv
dotenv.load_dotenv()

import openai, os, webbrowser, time
from app.helpers.prompt import format
from app.services.spotify import get_spotify_access_token, delete_spotify_playlist
from app.api.playlist import playlist

def main():
    # TODO: Token resets every hour. Remember to refresh in cron job?
    spotify_token = get_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET')) # type: ignore
    
    default = 'Motivational run at sunset'
    text = input(f"Prompt (default='{default}'): ") or default

    start = time.time()
    # create a chat completion
    playlist(spotify_token, text)

    # webbrowser.open(playlist_url)

    end = time.time()
    print(f"Time elapsed: {end-start} seconds")

    input("Hit [Enter] to delete.")

    # delete_spotify_playlist(playlist_id, os.getenv('SPOTIFY_HARDCODE_TOKEN'))

if __name__ == '__main__':
    main()
