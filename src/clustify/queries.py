"""

"""
import os
from tqdm import tqdm

import spotipy
from spotipy import SpotifyClientCredentials, SpotifyOAuth

from clustify.audio_feature_vector import FeatureVector, feature_vector_from_dict

CLUSTIFY_USER = os.getenv("CLIENT_SECRET", "be_cracked")

# TODO: Figure out what we really need
scopes = ["user-read-playback-state", "app-remote-control", "playlist-read-private", "playlist-read-collaborative",
          "user-read-currently-playing", "user-read-playback-position", "playlist-modify-private",
          "playlist-modify-public", "user-top-read", "streaming",
          "user-modify-playback-state", "user-read-recently-played",
          "user-library-read", "user-library-modify"]

# Use the SpotifyClientCredentials to authenticate with the Spotify API
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes), client_credentials_manager=client_credentials_manager)


def song_features_from_api(identifier: str) -> FeatureVector:
    audio_features = sp.audio_features(identifier)[0]
    return feature_vector_from_dict(audio_features)


def song_metadata_from_api(identifier: str) -> dict:
    metadata = sp.track(identifier)
    return metadata


def get_current_playback_uri():
    return sp.current_playback()["item"]["uri"]


# TODO: Refactor to allow to show also private playlists, add filter for public/private, names
def playlist_songs_from_api(username: str) -> dict[str, dict] | None:
    """
    Fetches the metadata and audio features for all playlists and metadata and groups them by playlist.
    """

    # Get all the playlists for the given user
    playlists = sp.user_playlists(username)
    if not playlists:
        return None

    playlist_data = {}

    # Iterate through each playlist and get the metadata for all the songs in the playlist
    for playlist in tqdm(playlists['items'], desc="Loading Playlist Metadata and Features"):
        playlist_uri = playlist['uri']
        playlist_name = playlist['name']
        playlist_tracks = sp.playlist_items(playlist_uri, additional_types=("track",))
        if not playlist_tracks:
            continue
        playlist_datum = {'uri': playlist_uri, 'name': playlist_name, 'tracks': []}
        for track_dict in playlist_tracks['items']:
            track = track_dict['track']
            uri = track['uri']
            audio_features = sp.audio_features(uri)[0]  # Returns a list with only one element
            song_metadata = {
                'uri': uri,
                'name': track['name'],
                'artists': track['artists'],
                'album': track['album'],
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity'],
                'explicit': track['explicit'],
                'audio_features': audio_features,
            }
            playlist_datum['tracks'].append(song_metadata)
        playlist_data[playlist_name] = playlist_datum

    return playlist_data
