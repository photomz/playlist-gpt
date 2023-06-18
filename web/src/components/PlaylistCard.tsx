import React from "react";

// Define the prop types for our component
interface PlaylistCardProps {
  title: string;
  description: string;
  imageUrl: string;
  onAdd: () => void;
}

export const PlaylistCard: React.FC<PlaylistCardProps> = ({
  title,
  description,
  imageUrl,
  onAdd,
}) => {
  return (
    <div className="flex items-center p-4 my-2 bg-white rounded-lg shadow-md">
      <div className="flex-shrink-0">
        <img
          className="h-24 w-24 rounded-lg shadow"
          src={imageUrl}
          alt={title}
        />
      </div>
      <div className="ml-6 pt-1">
        <div className="flex justify-start gap-4 items-center mb-2">
          <h4 className="text-xl text-black font-bold mr-4">{title}</h4>
          <button
            className="bg-teal-200 text-black p-2 sm:px-3 rounded-xl flex items-center"
            onClick={onAdd}
          >
            <p className="hidden text-base sm:inline sm:mr-1">Add to Spotify</p>
            <span className="material-symbols-outlined">add</span>
          </button>
          <button className="hidden sm:block bg-red-200 text-black p-2 sm:px-3 rounded-xl flex items-center">
            <span className="material-symbols-outlined">delete</span>
          </button>
        </div>
        <p className="text-base text-gray-700">{description}</p>
      </div>
    </div>
  );
};
