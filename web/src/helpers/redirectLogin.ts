export const redirectToLogin = () => {
  const params = new URLSearchParams({
    client_id: process.env.REACT_APP_SPOTIFY_CLIENT_ID as string,
    response_type: "code",
    redirect_uri: process.env.REACT_APP_SPOTIFY_REDIRECT_URI as string,
    scope:
      "user-read-private user-library-modify user-library-read user-top-read playlist-modify-public playlist-read-private user-read-currently-playing user-modify-playback-state ugc-image-upload",
  }).toString();

  window.location.href = `https://accounts.spotify.com/authorize?${params}`;
};

// WARN: url for Auth Lambda still in `PlaylistGPT` Hackthon folder - not this monorepo's Lambda
