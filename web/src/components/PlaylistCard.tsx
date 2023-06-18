import React from "react";

// Define the prop types for our component
interface PlaylistCardProps {
  title: string;
  description: string;
  imageUrl: string;
}

export const PlaylistCard: React.FC<PlaylistCardProps> = ({
  title,
  description,
  imageUrl,
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
        <h4 className="text-xl text-black font-bold mb-2">{title}</h4>
        <p className="text-base text-gray-700">{description}</p>
      </div>
    </div>
  );
};
