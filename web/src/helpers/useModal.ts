import React from "react";

// Create a custom hook for managing modal state
export const useModal = (initialState = false) => {
  const [isOpen, setIsOpen] = React.useState(initialState);

  const toggle = () => {
    setIsOpen(!isOpen);
  };

  return { isOpen, toggle };
};
