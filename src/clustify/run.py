import argparse as ap
import os
from pprint import pprint

from clustify.cache import save_playlist_data, load_playlist_data
from clustify.main import print_song_distances, playlist_clusters_from_dict
from clustify.queries import playlist_songs_from_api, get_current_playback_uri


def main():
    # TODO: Create and load config file
    parser = ap.ArgumentParser(prog="Clustify",
                               description="Tool for exploring songs and playlists in the Spotify vector space")
    parser.add_argument("--user", type=str, required=False, default=os.getenv("CLUSTIFY_USER", "be_cracked"),
                        help="The user who's public playlists to use. Defaults to env var 'CLUSTIFY_USER'")
    parser.add_argument("--cache_path", type=str, required=False, default="data/playlist_data.pkl")
    parser.add_argument("--refresh_cache", action="store_true")
    subparsers = parser.add_subparsers(title="sub parser")

    song_distance_parser = subparsers.add_parser("song_distance",
                                                 description="Show the distance to each playlist of the user")

    song_distance_parser.add_argument("song", type=str, default=None, nargs="?")

    args = parser.parse_args()

    if args.refresh_cache:
        playlist_data = playlist_songs_from_api("be_cracked")
        save_playlist_data(args.cache_path, playlist_data)
    playlist_data = load_playlist_data(args.cache_path)
    clusters = playlist_clusters_from_dict(playlist_data)

    song = args.song if args.song else get_current_playback_uri()
    print_song_distances(song, clusters)


if __name__ == '__main__':
    main()
