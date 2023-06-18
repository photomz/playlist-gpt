import React from "react";

// Define the prop types for our component
interface GalleryCardProps {
  title: string;
  description: string;
  imageUrl: string;
  onClick: () => void;
}

const iconStyle =
  "material-symbols-outlined text-white bg-gray-700 bg-opacity-50 rounded p-2";

export const GalleryCard: React.FC<GalleryCardProps> = ({
  title,
  description,
  imageUrl,
  onClick,
}) => {
  return (
    <div
      className="relative group overflow-hidden rounded-lg shadow-md cursor-pointer w-64 h-64"
      onClick={onClick}
    >
      <img className="w-full h-full object-cover" src={imageUrl} alt={title} />
      <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-colors duration-200 ease-out" />
      <div className="absolute top-0 left-0 p-2 group-hover:block hidden">
        <span className={iconStyle}>search</span>
      </div>
      <div className="absolute top-0 right-0 gap-3 p-2 group-hover:flex flex-col hidden">
        <span className={iconStyle}>play_arrow</span>
        <span className={iconStyle}>add</span>
      </div>
      <div className="absolute bottom-0 left-0 p-2 text-white group-hover:block hidden">
        <h3 className="font-bold">{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
};
