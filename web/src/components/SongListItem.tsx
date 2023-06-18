import React from "react";
import { Preview } from "../api/spotify";
import { DivCallback } from "../helpers/util";

export const SongListItem = ({
  preview,
  detail,
  num,
  maxNum,
  omitType,
  onPlay,
  onClick,
}: {
  preview: Preview; // Will display <p>type</p> if TypedPreview
  detail?: boolean;
  num?: number;
  maxNum?: number;
  omitType?: boolean;
  onPlay: DivCallback;
  onClick: DivCallback;
}) => (
  <div
    className={
      "relative flex flex-row items-center shadow-md rounded-md mb-2 max-w-full overflow-hidden cursor-pointer" +
      (detail ? " bg-gray-200 bg-opacity-70" : "") +
      (preview.disabled ? " text-[#888] opacity-50 pointer-events-none" : "")
    }
    onClick={(e) => (preview.type === "playlist" ? onClick(e) : onPlay(e))} // TODO: Toast on failure
  >
    {num && maxNum && (
      <div className="flex-none flex flex-col justify-between items-center box-content py-2 w-10">
        <p className="text-xl text-gray-800">{num}</p>
      </div>
    )}
    <div className="h-12 w-12 mr-2 flex-none relative">
      <img
        src={preview.albumUrl}
        alt="Album cover"
        className={"object-cover" + (preview.disabled && "opacity-40")}
      />
    </div>
    <div className="text-left truncate mr-auto">
      <p className="font-bold truncate">{preview.name}</p>
      <p className="text-tiny truncate text-gray-800 capitalize">
        {preview.type && !omitType && preview.type + " • "}
        {preview.author}
      </p>
    </div>
    {detail && preview.type === "song" && (
      <div
        className={
          "flex-none flex justify-center items-center h-12 w-12" +
          (preview.disabled ? " opacity-50" : "")
        }
        onClick={(e) => {
          e.stopPropagation();
          onClick(e);
        }}
      >
        {">"}
      </div>
    )}
  </div>
);
