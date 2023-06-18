import React, { useState, useEffect } from "react";

export const AudioContext = React.createContext(null);

export function AudioProvider({ children }) {
  const [audio, setAudio] = useState(null);
  const [source, setSource] = useState("");

  useEffect(() => {
    // Only pause current audio if new source is set
    if (audio && source) {
      audio.pause();
      setAudio(null);
    }
    console.log("New source", source);
    if (source) {
      const newAudio = new Audio(source);
      setAudio(newAudio);
      newAudio.play();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [source]);

  return (
    <AudioContext.Provider value={{ audio, setSource }}>
      {children}
    </AudioContext.Provider>
  );
}
