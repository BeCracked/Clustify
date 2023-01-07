import logging
from collections import defaultdict
from pprint import pprint
import numpy as np

from clustify.audio_feature_vector import normalize_feature_vector, feature_vector_from_dict, audio_feature_properties
from clustify.cache import load_playlist_data, save_playlist_data
from clustify.playlist_cluster import PlaylistCluster
from clustify.queries import playlist_songs_from_api, song_features_from_api, song_metadata_from_api

logger = logging.getLogger()


def playlist_clusters_from_dict(playlist_data: dict) -> dict[str, PlaylistCluster]:
    playlist_clusters = {}
    for playlist, data in playlist_data.items():
        playlist_clusters[playlist] = PlaylistCluster(data["uri"], data["name"], data["tracks"])
    return playlist_clusters


def condense_playlists_to_clusters(playlist_data: dict) -> dict[str, dict]:
    # Transform playlists to list of features
    feature_vectors = defaultdict(list)
    for playlist, metadata in playlist_data.items():
        for track in metadata:
            audio_features = track["audio_features"]
            vec = feature_vector_from_dict(audio_features)
            vec = normalize_feature_vector(vec)
            feature_vectors[playlist].append(np.asarray(vec))

    # TODO: Calculate mean and std per playlist
    # Distance function?
    clusters = {}
    for playlist, song_features in feature_vectors.items():
        clusters[playlist] = {"mean": np.mean(song_features, axis=0), "std": np.std(song_features, axis=0)}

    i = 0
    by_features = {}
    for feature in audio_feature_properties:
        feature_only = {pl: fv["mean"][i] for pl, fv in clusters.items()}
        by_features[feature] = list(sorted(feature_only, key=feature_only.get, reverse=True))
        i += 1

    return dict(feature_vectors)


def print_song_distances(identifier: str, clusters: dict[str, PlaylistCluster], *, max_playlists: int = 10):
    metadata = song_metadata_from_api(identifier)
    song_vec = song_features_from_api(identifier)
    distance_dict = {pl_name: round(cl.get_distance_to(song_vec), 3) for pl_name, cl in clusters.items()}
    print(f"Song: {metadata['name']} - {metadata['artists'][0]['name']}")
    pprint(list(sorted(distance_dict.items(), key=lambda x: x[1]))[:max_playlists])


def main(refresh_cache: bool = False):
    path = "../data/playlist_data.pkl"
    if refresh_cache:
        playlist_data = playlist_songs_from_api("be_cracked")
        save_playlist_data(path, playlist_data)
    playlist_data = load_playlist_data(path)
    clusters = playlist_clusters_from_dict(playlist_data)
    #songs = list(itertools.chain(*list(playlist_data.values())))


if __name__ == "__main__":
    main(refresh_cache=False)

    example_item = {
        'added_at': '2020-02-24T09:01:38Z',
        'added_by': {'external_urls': {'spotify': 'https://open.spotify.com/user/be_cracked'},
                     'href': 'https://api.spotify.com/v1/users/be_cracked', 'id': 'be_cracked', 'type': 'user',
                     'uri': 'spotify:user:be_cracked'},
        'is_local': False, 'primary_color': None,
        'track': {
            'album': {
                'album_type': 'single',
                'artists': [
                    {'external_urls': {'spotify': 'https://open.spotify.com/artist/7zgtAvNKkyrcJG2Ad1M1Kv'},
                     'href': 'https://api.spotify.com/v1/artists/7zgtAvNKkyrcJG2Ad1M1Kv',
                     'id': '7zgtAvNKkyrcJG2Ad1M1Kv', 'name': 'POM', 'type': 'artist',
                     'uri': 'spotify:artist:7zgtAvNKkyrcJG2Ad1M1Kv'}],
                'available_markets': [],
                'external_urls': {'spotify': 'https://open.spotify.com/album/0sHfq6jCbGAXn64YQSC77c'},
                'href': 'https://api.spotify.com/v1/albums/0sHfq6jCbGAXn64YQSC77c',
                'id': '0sHfq6jCbGAXn64YQSC77c',
                'images': [{'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b273d90973bb492164ed36769dfd',
                            'width': 640},
                           {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e02d90973bb492164ed36769dfd',
                            'width': 300},
                           {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d00004851d90973bb492164ed36769dfd',
                            'width': 64}],
                'name': 'Down The Rabbit Hole',
                'release_date': '2019-05-17',
                'release_date_precision': 'day',
                'total_tracks': 1, 'type': 'album', 'uri': 'spotify:album:0sHfq6jCbGAXn64YQSC77c'},
            'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/7zgtAvNKkyrcJG2Ad1M1Kv'},
                         'href': 'https://api.spotify.com/v1/artists/7zgtAvNKkyrcJG2Ad1M1Kv',
                         'id': '7zgtAvNKkyrcJG2Ad1M1Kv', 'name': 'POM', 'type': 'artist',
                         'uri': 'spotify:artist:7zgtAvNKkyrcJG2Ad1M1Kv'}],
            'available_markets': [], 'disc_number': 1,
            'duration_ms': 195306,
            'episode': False,
            'explicit': False,
            'external_ids': {'isrc': 'QZES81996602'},
            'external_urls': {'spotify': 'https://open.spotify.com/track/7be2yV2uez1VhXyPN4HQYg'},
            'href': 'https://api.spotify.com/v1/tracks/7be2yV2uez1VhXyPN4HQYg',
            'id': '7be2yV2uez1VhXyPN4HQYg',
            'is_local': False,
            'name': 'Down The Rabbit Hole',
            'popularity': 0,
            'preview_url': None,
            'track': True, 'track_number': 1, 'type': 'track', 'uri': 'spotify:track:7be2yV2uez1VhXyPN4HQYg'},
        'video_thumbnail': {'url': None}
    }

    audio_feature = [
        {'danceability': 0.488,
         'energy': 0.868,
         'key': 8,
         'loudness': -5.266,
         'mode': 1,
         'speechiness': 0.0333,
         'acousticness': 0.00615,
         'instrumentalness': 0.0169,
         'liveness': 0.0877,
         'valence': 0.345,
         'tempo': 156.996,
         'type': 'audio_features',
         'id': '3Iq8XToI0I9KSnqovkv1AV',
         'uri': 'spotify:track:3Iq8XToI0I9KSnqovkv1AV',
         'track_href': 'https://api.spotify.com/v1/tracks/3Iq8XToI0I9KSnqovkv1AV',
         'analysis_url': 'https://api.spotify.com/v1/audio-analysis/3Iq8XToI0I9KSnqovkv1AV',
         'duration_ms': 210191,
         'time_signature': 4}]
{'Wohlfühl Indie': [
    {'song_uri': 'spotify:track:3Iq8XToI0I9KSnqovkv1AV', 'song_name': 'Vertigo', 'artist_name': 'Edwin Rosen',
     'album_name': 'Vertigo', 'duration_ms': 210191, 'popularity': 65, 'audio_features': [
        {'danceability': 0.488, 'energy': 0.868, 'key': 8, 'loudness': -5.266, 'mode': 1, 'speechiness': 0.0333,
         'acousticness': 0.00615, 'instrumentalness': 0.0169, 'liveness': 0.0877, 'valence': 0.345, 'tempo': 156.996,
         'type': 'audio_features', 'id': '3Iq8XToI0I9KSnqovkv1AV', 'uri': 'spotify:track:3Iq8XToI0I9KSnqovkv1AV',
         'track_href': 'https://api.spotify.com/v1/tracks/3Iq8XToI0I9KSnqovkv1AV',
         'analysis_url': 'https://api.spotify.com/v1/audio-analysis/3Iq8XToI0I9KSnqovkv1AV', 'duration_ms': 210191,
         'time_signature': 4}]}]}
