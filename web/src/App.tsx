import { SongListItem } from "./components/SongListItem";
import _ from "lodash";
import playlistData from "./assets/playlist.json";

import React, { useState } from "react";
import { Playlist } from "./api/playlist";

const InputComponent = ({ onSubmit }) => {
  const [inputValue, setInputValue] = useState("");

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(inputValue);
    setInputValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-row">
      <input
        className="bg-zinc-700 flex-1 pl-12 pr-12 rounded-full text-sm px-4 py-2.5 focus:outline-none focus:ring-1 focus:ring-indigo-700"
        placeholder="Search for a playlist"
        type="text"
        value={inputValue}
        onChange={handleChange}
      />
      <button
        className="w-32 sm:w-36 flex items-center text-xs justify-center text-center  h-9 rounded-full  hover:brightness-110 bg-opacity-0 shadow-sm  mt-4 bg-gradient-to-t bg-gray-200 text-black"
        type="submit"
      >
        Generate
      </button>
    </form>
  );
};

export const App = () => {
  const [playlist, setPlaylist] = useState<Playlist | null>(playlistData);

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
      setPlaylist(null);
    }
  };
  return (
    <section className="bg-teal-100 relative px-4 mt-4">
      <InputComponent onSubmit={onSubmit} />
      {playlist?.songs?.map((song, i) => (
        <SongListItem song={song} num={i + 1} key={`${song.id}-${i}`} />
      ))}
    </section>
  );
};
