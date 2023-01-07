from dataclasses import dataclass, field, InitVar

import numpy as np
import pandas as pd

from clustify.audio_feature_vector import feature_vector_from_dict, normalize_feature_vector, FeatureVector, \
    distance

track_properties = ["uri", "name", "duration_ms", "explicit", "album", "artists", "audio_features"]
album_properties = ["artists", "uri", "name", "total_tracks", "release_date"]
artists_properties = ["uri", "name"]


@dataclass()
class PlaylistCluster:
    uri: str
    name: str
    tracks: list[dict] = field(init=False, repr=False, hash=False, compare=False)
    track_dicts: InitVar[list[dict] | None] = None  # Input tracks
    # Calculated properties
    df: pd.DataFrame = field(init=False, repr=False, hash=False, compare=False)
    mean_coordinates: np.array = field(init=False, repr=False, hash=False, compare=False)
    mean_per_feature: dict[str, float] = field(init=False, repr=False, hash=False, compare=False)
    std: float = field(init=False, repr=False, hash=False, compare=False)
    std_per_feature: dict[str, float] = field(init=False, repr=False, hash=False, compare=False)

    def __post_init__(self, track_dicts):
        # filter track dicts
        self.tracks = []
        for track_dict in track_dicts:
            track = {key: track_dict.get(key, None) for key in track_properties}
            track["album"] = {key: track["album"] for key in album_properties}
            track["artists"] = {key: track["artists"] for key in artists_properties}
            track["audio_features"] = track["audio_features"]
            self.tracks.append(track)

        # Fill dataframe
        feature_vectors = []
        for track in self.tracks:
            audio_features = track["audio_features"]
            vec = normalize_feature_vector(feature_vector_from_dict(audio_features))
            feature_vectors.append((track["name"], *vec))
        self.df = pd.DataFrame(feature_vectors, columns=["track", *list(FeatureVector._fields)])
        self.mean_coordinates = self.df.mean(numeric_only=True).to_numpy()

    def get_mean_distance(self, *, feature_list: list = None):
        """
        Get the mean distance of all songs to the mean coordinates of this playlist.
        Returns
        -------

        """


    def get_distance_to(self, vec: FeatureVector | dict | np.ndarray, *, feature_list: list = None):
        return distance(FeatureVector(*self.mean_coordinates), vec, feature_list=feature_list)
