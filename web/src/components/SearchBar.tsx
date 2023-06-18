import React, { useState } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
  onGenerate: (query: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  onGenerate,
}) => {
  const [query, setQuery] = useState("");
  const [submitType, setSubmitType] = useState<"search" | "generate">("search");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (submitType === "search") {
      onSearch(query);
    } else {
      onGenerate(query);
    }
  };

  return (
    <form className="flex flex-col items-center p-4" onSubmit={handleSubmit}>
      <div className="flex items-center bg-white rounded-full w-full px-3 focus-within:ring-2 focus-within:ring-blue-500">
        <span className="fill-current text-gray-600 h-5 w-5 mb-0.5 material-symbols-outlined">
          search
        </span>
        <input
          className="ml-2 w-full p-2 rounded-full outline-none"
          type="text"
          placeholder="Search..."
          value={query}
          onChange={handleInputChange}
        />
      </div>
      <div className="flex justify-center mt-4">
        <button
          className="bg-teal-200 text-black rounded-xl px-4 py-2 mr-2"
          type="submit"
          onClick={() => setSubmitType("search")}
        >
          Search
        </button>
        <button
          className="bg-white text-black rounded-xl px-4 py-2 ml-2"
          type="submit"
          onClick={() => setSubmitType("generate")}
        >
          Generate
        </button>
      </div>
    </form>
  );
};
