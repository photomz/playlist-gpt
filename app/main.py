import openai, os, dotenv, yaml
from prompt import format
from unsplash import batch_search_unsplash
from spotify import get_spotify_access_token, batch_search_spotify

dotenv.load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

spotify_token = get_spotify_access_token(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET')) # type: ignore

# End setup

input = "Running at dawn" #input()
prompt = format(input)

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

image_url = batch_search_unsplash([yaml_completion['image']], [1])[0][0]
print(image_url)

song_ids = batch_search_spotify(yaml_completion['tracks'], spotify_token) # type: ignore
print(song_ids)