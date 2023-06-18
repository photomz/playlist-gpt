import fetch from "isomorphic-fetch";
import _ from "lodash";
import { redirectToLogin } from "../helpers/redirectLogin";
import { dbg, openInApp, wait } from "../helpers/util";

export type Preview = {
  name: string;
  type: "song" | "playlist";
  albumUrl: string;
  author: string;
  _id: string;
  url: string;
  duration?: string;
  disabled?: boolean; // If vector doesn't exist, can't click Preview to find similar
  // -> If playlist, not song, doesn't exist ->
  // -> Or if album has many disks, "offset" in Spotify /player/play doesn't work, so exclude ->
  albumId?: string;
  numInAlbum?: number;
};

const authorisedFetch = async (url: string, options?: any): Promise<any> => {
  const res: Response = await fetch(
    url,
    _.merge(options, {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
  );

  // Access code expired - force refresh page to repeat access token process
  if (res.status === 401) {
    redirectToLogin();
    return {};
  } else if (res.status === 204) {
    return {};
  } else if (res.status === 429) {
    const depth: number = options?.depth ?? 0;
    if (options?.retry === true && depth < 10) {
      dbg(`Throttled (${depth}) ${url}`);
      await wait(500 * depth);
      return authorisedFetch(url, { ...options, depth: depth + 1 });
    } else {
      console.error(
        "Client is requesting Spotify endpoints too frequently. Please cool down."
      );
    }
  }
  return res.json();
};

export const disableShuffle = async () =>
  authorisedFetch("https://api.spotify.com/v1/me/player/shuffle?state=false", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
  });

// TODO: Only queue after remote open
// TODO: Deal with HTTP 403 "Restricted Device" on Sonos External Speaker - error toast asking user to manually change sound output device
export const playSongsWithoutContext = async (
  songIds: string[],
  urls: string[],
  depth?: number
): Promise<any> => {
  depth = depth ?? 0;
  await disableShuffle();
  const res = await authorisedFetch(
    "https://api.spotify.com/v1/me/player/play",
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        uris: songIds.map((id) => `spotify:track:${id}`),
      }),
    }
  );
  if (
    res?.error?.status === 404 &&
    res?.error?.reason === "NO_ACTIVE_DEVICE" &&
    !depth
  ) {
    window.open(openInApp(urls[0])); // Force autoplay by opening Spotify app - create active device
    await playSongsWithoutContext(songIds, urls, 1);
  }
  return res;
};

export const playSong = async (song: Preview, depth?: number): Promise<any> => {
  depth = depth ?? 0;
  if (song.type !== "song") {
    console.error(
      `To playSong, Preview must be of type song, not "${song.type}".`
    );
    return Promise.reject();
  }
  const body =
    song?.albumId && song?.numInAlbum
      ? {
          context_uri: `spotify:album:${song.albumId}`,
          offset: { position: song.numInAlbum - 1 }, // 0/1-indexing
        }
      : { uris: [`spotify:track:${song._id}`] };
  const res = await authorisedFetch(
    "https://api.spotify.com/v1/me/player/play",
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }
  );
  if (
    res?.error?.status === 404 &&
    res?.error?.reason === "NO_ACTIVE_DEVICE" &&
    !depth
  ) {
    window.open(openInApp(song.url)); // Force autoplay by opening Spotify app - create active device
    await playSong(song, 1);
  }
  return res;
};

export const playPlaylist = async (
  playlist: Preview,
  depth?: number
): Promise<any> => {
  depth = depth ?? 0;
  if (playlist.type !== "playlist") {
    console.error(
      `To playPlaylist, Preview must be of type playlist, not "${playlist.type}".`
    );
    return Promise.reject();
  }
  const res = await authorisedFetch(
    "https://api.spotify.com/v1/me/player/play",
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        context_uri: `spotify:playlist:${playlist?._id}`,
      }),
    }
  );
  if (
    res?.error?.status === 404 &&
    res?.error?.reason === "NO_ACTIVE_DEVICE" &&
    !depth
  ) {
    window.open(openInApp(playlist.url)); // Force autoplay by opening Spotify app - create active device
    await playPlaylist(playlist, 1);
  }
  return res;
};

export const queueSong = async (songId: string, url: string): Promise<any> => {
  const res = await authorisedFetch(
    `https://api.spotify.com/v1/me/player/queue?uri=spotify%3Atrack%3A${songId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (res?.error?.status === 404 && res?.error?.reason === "NO_ACTIVE_DEVICE") {
    window.open(openInApp(url)); // Force autoplay by opening Spotify app - create active device
  }
  return res;
};
