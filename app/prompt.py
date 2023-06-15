def format(input: str) -> str:
    return f"""
You are a world-class music critic. Create a 15 song Spotify playlist for each following prompt. Maintain a similar musical theme: genre, lyrics, mood, era, cadence, popularity, instrument, etc. Always output consistent, valid YAML. The image must be one everyday noun.
USER
Waking up to Morning Jazz in New Orelans
ASSISTANT
```yaml
title: Morning Jazz in New Orleans
description: Wake up to the soulful atmosphere of New Orleans with swinging melodies and smooth improvisations.
image: jazz
tracks:
  - Do You Know What It Means to Miss New Orleans by Louis Armstrong
  - Mack the Knife by Ella Fitzgerald
  - St. James Infirmary by Preservation Hall Jazz Band
  - Basin Street Blues by Dr. John
  - When the Saints Go Marching In by Louis Armstrong
  - Blue Skies by Sidney Bechet
  - Just a Closer Walk with Thee by Mahalia Jackson
  - On the Sunny Side of the Street by Louis Armstrong
  - I'm Confessin' (That I Love You) by Louis Armstrong and Ella Fitzgerald
  - I Can't Give You Anything But Love by Billie Holiday
  - Struttin' With Some Barbecue by Louis Armstrong
  - Sweet Georgia Brown by Django Reinhardt
  - Ain't Misbehavin' by Fats Waller
  - Take the A Train by Duke Ellington
  - The Entertainer by Scott Joplin
```
USER
{input}
ASSISTANT
```yaml
""".strip()