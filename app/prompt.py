def format(input: str) -> str:
    return f"""
USER
You are a world-class musician. Create a beautiful, popular Spotify playlist with 15 songs for each following prompt. Maintain a similar musical theme: genre, lyrics, mood, era, instrument, etc. Always output consistent, valid YAML. The image must be one everyday noun, and only include the artist's name for rare songs.
USER
Falling in love on a spring morning
ASSISTANT
```yaml
title: Spring Fever Romance
description: Fall in love all over again with these love songs perfect for a crisp spring morning.
image: spring
tracks:
  - Like I'm Going to Lose You
  - Make You Feel My Love
  - Can't Help Falling in Love
  - At Last
  - Just the Way You Are
  - A Thousand Years by Christina Perri
  - Thinking Out Loud
  - Perfect
  - All of Me
  - I Choose You by Sara Bareilles
```
USER
{input}
ASSISTANT
```yaml
""".strip()