from app.services.spotify import create_spotify_playlist


def spotify(songs, user_token, username, title, description, image):
    # TODO: Get songs, title, description, image from db not params
    song_ids = (song['id'] for song in songs)
    playlist_url, playlist_id = create_spotify_playlist(
        title=title,
        description=f"{description} (made by playlist-gpt)",
        track_ids=song_ids,
        image_url=image,
        access_token=user_token, #os.getenv('SPOTIFY_HARDCODE_TOKEN'),
        user_id=username #os.getenv('SPOTIFY_HARDCODE_ID')
    )
    return playlist_url, playlist_id