import playlistData from "./assets/playlist.json";

import React, { useState } from "react";
import { Playlist, SpotifyPlaylist } from "./api/playlist";
import { PlaylistCard } from "./components/PlaylistCard";
import { SongItem } from "./components/SongItem";
import { SearchBar } from "./components/SearchBar";
import { openInApp } from "./helpers/util";
import { AudioProvider } from "./components/AudioContext";

export const App = () => {
  const [playlist, setPlaylist] = useState<Playlist>(playlistData);

  const onSubmit = async (query: string) => {
    try {
      const response = await fetch(`http://localhost:8000/playlist`, {
        method: "POST",
        body: JSON.stringify({ prompt: query }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data: Playlist = await response.json(); // Parse the response JSON

      console.log(data);
      setPlaylist(data);
    } catch (error) {
      console.error(error);
      setPlaylist(playlistData);
    }
  };

  const onAddToSpotify = async () => {
    try {
      const response = await fetch(`http://localhost:8000/spotify`, {
        method: "POST",
        body: JSON.stringify({
          id: playlist.id,
          username: localStorage.getItem("id"),
          user_token: localStorage.getItem("token"),
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data: SpotifyPlaylist = await response.json(); // Parse the response JSON

      console.log(data);

      window.open(openInApp(data.url));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <AudioProvider>
      <section className="bg-teal-100 relative px-4">
        <SearchBar onSearch={onSubmit} onGenerate={onSubmit} />
        <PlaylistCard
          title={playlist?.title}
          description={playlist?.description}
          imageUrl={playlist?.image_url}
          onAdd={onAddToSpotify}
        />
        {playlist?.songs?.map((song, i) => (
          <SongItem song={song} track_num={i + 1} key={`${song.id}-${i}`} />
        ))}
      </section>
    </AudioProvider>
  );
};
