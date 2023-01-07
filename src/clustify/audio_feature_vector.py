from collections import namedtuple

import numpy
import scipy

audio_feature_properties = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                            "instrumentalness", "liveness", "valence", "tempo"]
# Subset of audio features to consider by default for the distance function
default_distance_features = ["danceability", "energy", "key", "loudness", "speechiness", "acousticness",
                             "instrumentalness", "liveness", "valence", "tempo"]
# TODO: Refactor as DataClass
FeatureVector = namedtuple("FeatureVector", audio_feature_properties)

MIN_MAX_DICT = {
    "loudness": {"min": -60, "max": 0},
    "tempo": {"min": 30, "max": 250},
    "key": {"min": -1, "max": 11},  # As per API specs. TODO: Check whether other distancing would make more sense
}


def normalize_feature_vector(feature_vector: FeatureVector,
                             min_max_dict: dict[str, dict[str, float | int]] = None) -> FeatureVector:
    """
    Normalizes features that are not already in a normalized form. Min-Max normalization to a range of [0,1] is used.

    Parameters
    ----------
    feature_vector The feature vector to normalize.
    min_max_dict The features to normalize with their respective min/max values.
    """
    min_max_dict = min_max_dict if min_max_dict else MIN_MAX_DICT

    val_dict = feature_vector._asdict()
    for feature, limits in min_max_dict.items():
        val, v_min, v_max = val_dict[feature], limits["min"], limits["max"]
        val_dict[feature] = (val - v_min) / (v_max - v_min)

    return FeatureVector(**val_dict)


def feature_vector_from_dict(audio_features: dict):
    return FeatureVector(**{key: audio_features[key] for key in audio_feature_properties})


def distance(vec1: FeatureVector | dict | numpy.ndarray, vec2: FeatureVector | dict | numpy.ndarray,
             *, feature_list: list = None):
    """
    Gets the distance between two feature vector likes
    by taking the euclidean distance over the given feature list or the defaults

    Parameters
    ----------
    vec1 Either a FeatureVector or dict with all keys in feature_list or an array_like.
         If an array_like it needs to be certain that the order of the properties match.
    vec2 Either a FeatureVector or dict with all keys in feature_list or an array_like.
         If an array_like it needs to be certain that the order of the properties match.
    feature_list List of features to consider

    Returns
    -------

    """
    feature_list = feature_list if feature_list else default_distance_features
    # Aggregate features
    vec1 = vec1 if not isinstance(vec1, FeatureVector) else normalize_feature_vector(vec1)._asdict()
    if isinstance(vec1, dict):
        features1 = []
        for feature in feature_list:
            features1.append(vec1[feature])
        vec1 = numpy.array(features1)
    vec2 = vec2 if not isinstance(vec2, FeatureVector) else normalize_feature_vector(vec2)._asdict()
    if isinstance(vec2, dict):
        features2 = []
        for feature in feature_list:
            features2.append(vec2[feature])
        vec2 = numpy.array(features2)

    return scipy.spatial.distance.euclidean(vec1, vec2)
