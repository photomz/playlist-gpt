import React, { useState } from "react";
import { Song } from "../api/playlist";

// We are now using the provided Song interface
interface SongItemProps {
  song: Song;
  track_num: number; // Track number in playlist
}

export const SongItem: React.FC<SongItemProps> = ({ song, track_num }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audio = new Audio(song.audio_url || "");

  const toggleAudio = () => {
    if (!isPlaying) {
      audio.play();
    } else {
      audio.pause();
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="flex items-center p-2 cursor-pointer" onClick={toggleAudio}>
      <span className="text-gray-500 mr-4">{track_num}</span>
      <img className="h-full w-10 mr-4" src={song.image_url} alt={song.name} />
      <div>
        <h5 className="text-md font-semibold mb-1">{song.name}</h5>
        <p className="text-sm text-gray-500">{song.artist}</p>
      </div>
    </div>
  );
};
