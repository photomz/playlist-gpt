export interface SpotifyPlaylist {
  id: string;
  spotify_id: string;
  username: string;
  url: string;
}

export interface Song {
  id: string; // Spotify ID
  name: string;
  artist: string;
  album: string;
  year: string;
  url: string;
  album_id: string;
  track_num: number;
  duration_ms: number;
  image_url: string; // Album image URL
  audio_url?: string; // Spotify audio URL, not available for all songs
}

export interface Playlist {
  id: string;
  title: string;
  description: string;
  image_url: string;
  prompt: string;
  audio_url: string;
  songs: Song[];
}
