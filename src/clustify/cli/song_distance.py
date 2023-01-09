import argparse

from clustify.cache import load_playlist_data
from clustify.main import print_song_distances, playlist_clusters_from_dict
from clustify.queries import get_current_playback_uri


def add_song_distance_parser(subparsers: argparse._SubParsersAction):  # noqa: _SubParsersAction
    song_distance_parser: argparse.ArgumentParser = subparsers.add_parser(
        name="song_distance",
        aliases=["sd"],
        description="Show the distance to each playlist of the user")
    song_distance_parser.add_argument("song", type=str, default=None, nargs="?")

    song_distance_parser.set_defaults(func=handle)


def handle(args):
    song = args.song if args.song else get_current_playback_uri()
    playlist_data = load_playlist_data(args.cache_path)
    clusters = playlist_clusters_from_dict(playlist_data)
    print_song_distances(song, clusters)
