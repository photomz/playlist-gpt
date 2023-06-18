import openai, os, yaml, random
from dataclasses import dataclass, field
from typing import List
from app.helpers.prompt import format
from app.services.unsplash import batch_search_unsplash
from app.services.spotify import get_spotify_access_token, batch_search_spotify, Playlist

openai.api_key = os.getenv('OPENAI_API_KEY')

spotify_token = get_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET')) # type: ignore

# End setup
def playlist(spotify_token, text):
    prompt = format(text)
    raw_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stop=['```'],
        temperature=0.7
    )

    # print the chat completion
    completion = raw_completion.choices[0].message.content # type: ignore
    print(completion)

    yaml_completion = yaml.safe_load(completion)
    print(yaml_completion)

    image_url = random.choice(batch_search_unsplash([yaml_completion['image']], [5])[0])
    print(image_url)

    # [{title, artist}] -> [titles], [artists]
    titles = [key for _dict in yaml_completion['tracks'] for key in _dict.keys()]
    artists = [value for _dict in yaml_completion['tracks'] for value in _dict.values()]

    songs = batch_search_spotify(titles, artists, spotify_token) # type: ignore
    song_ids = [song.id for song in songs if song]
    print(song_ids)

    playlist = Playlist(
        id='', # TODO: our db id
        title=yaml_completion['title'],
        description=yaml_completion['description'],
        image_url=image_url,
        prompt=prompt,
        audio_url='', # TODO: generate 3sec clips per song
        songs=songs
    )

    return playlist