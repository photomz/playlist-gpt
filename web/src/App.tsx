import { SongListItem } from "./components/SongListItem";
import { playSong, Preview } from "./api/spotify";
import { MouseEvent } from "react";
import _ from "lodash";
import songData from "./assets/songs.json";

export const App = () => (
  <section className="bg-teal-100 relative px-4 mt-4">
    {songData.map((preview, i) => (
      <SongListItem
        detail
        omitType
        preview={preview}
        num={i + 1}
        maxNum={songData.length}
        key={`${preview._id}-${i}`}
        onPlay={_.partialRight(
          (e: MouseEvent<HTMLDivElement>, preview: Preview) => {
            e.stopPropagation();
            playSong(preview);
          },
          preview
        )}
        onClick={_.partialRight(() => {}, preview)}
      />
    ))}
  </section>
);
