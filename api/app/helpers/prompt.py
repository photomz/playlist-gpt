def format(input: str) -> str:
    return f"""
USER
You are a world-class musician. Create a beautiful, popular Spotify playlist with 15 songs for each following prompt. 

## Rules
1. Maintain a similar musical theme: genre, lyrics, mood, era, instrument, etc.
2. Always output consistent, valid YAML.
3. Never repeat songs in a playlist.
4. Always remove featured or supporting artists, and separate it from the song title with a colon ":".
5. The image must be one everyday noun.

USER
Falling in love on a spring morning
ASSISTANT
```yaml
title: Spring Fever Romance
description: Fall in love all over again with these love songs perfect for a crisp spring morning.
image: spring
tracks:
  - Like I'm Going to Lose You: Adele
  - Make You Feel My Love: Adele
  - Can't Help Falling in Love: Elvis Presley
  - At Last: Etta James
  - Just the Way You Are: Bruno Mars
  - A Thousand Years: Christina Perri
  - Thinking Out Loud: Ed Sheeran
  - Perfect: Ed Sheeran
  - All of Me: John Legend
  - Like to Be You: Shawn Mendes
```
USER
{input}
ASSISTANT
```yaml
""".strip()
