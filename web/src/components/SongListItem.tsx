import React from "react";
import { Song } from "../api/playlist";

export const SongListItem = ({ song, num }: { song: Song; num?: number }) => (
  <div
    className={
      "relative flex flex-row items-center shadow-md rounded-md mb-2 max-w-full overflow-hidden cursor-pointer" +
      " bg-gray-200 bg-opacity-70"
    }
    onClick={() => {}} // TODO: Audio playback
  >
    {num && (
      <div className="flex-none flex flex-col justify-between items-center box-content py-2 w-10">
        <p className="text-xl text-gray-800">{num}</p>
      </div>
    )}
    <div className="h-12 w-12 mr-2 flex-none relative">
      <img src={song.image_url} alt="Album cover" className="object-cover" />
    </div>
    <div className="text-left truncate mr-auto">
      <p className="font-bold truncate">{song.name}</p>
      <p className="text-tiny truncate text-gray-800 capitalize">
        {song.artist}
      </p>
    </div>
  </div>
);
