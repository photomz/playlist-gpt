import openai, os, dotenv, yaml, webbrowser, random, time
from prompt import format
from unsplash import batch_search_unsplash
from spotify import get_spotify_access_token, batch_search_spotify, create_spotify_playlist, delete_spotify_playlist

dotenv.load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

spotify_token = get_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET')) # type: ignore

# End setup

default = 'Motivational run at sunset'
text = input(f"Prompt (default='{default}'): ") or default
prompt = format(text)

start = time.time()
# create a chat completion
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

songs = batch_search_spotify(yaml_completion['tracks'], spotify_token) # type: ignore
song_ids = [song.id for song in songs if song]
print(song_ids)

playlist_url, playlist_id = create_spotify_playlist(
    title=yaml_completion['title'],
    description=f"{yaml_completion['description']} (made by playlist-gpt)",
    track_ids=song_ids,
    image_url=image_url,
    access_token=os.getenv('SPOTIFY_HARDCODE_TOKEN'),
    user_id=os.getenv('SPOTIFY_HARDCODE_ID')
)
print(playlist_url)

webbrowser.open(playlist_url) # type: ignore

end = time.time()
print(f"Time elapsed: {end-start} seconds")

input("Hit [Enter] to delete.")

delete_spotify_playlist(playlist_id, os.getenv('SPOTIFY_HARDCODE_TOKEN'))