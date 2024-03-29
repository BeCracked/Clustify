import os
import pickle


def save_playlist_data(path, playlist_metadata: dict):
    if not playlist_metadata:
        return

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w+b") as f:
        pickle.dump(playlist_metadata, f)
    print(f"Saved playlist data to {path!r}")
    return playlist_metadata


def load_playlist_data(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
        return data
