import argparse as ap
import os

from clustify.cache import save_playlist_data
from clustify.cli.song_distance import add_song_distance_parser
from clustify.queries import playlist_songs_from_api


def main():
    # TODO: Create and load config file
    parser = ap.ArgumentParser(prog="Clustify",
                               description="Tool for exploring songs and playlists in the Spotify vector space")
    parser.add_argument("--user", type=str, required=False, default=os.getenv("CLUSTIFY_USER", "be_cracked"),
                        help="The user who's public playlists to use. Defaults to env var 'CLUSTIFY_USER'")
    parser.add_argument("--cache_path", type=str, required=False, default="data/playlist_data.pkl")
    parser.add_argument("--refresh_cache", action="store_true")
    subparsers = parser.add_subparsers(title="sub parser")
    add_song_distance_parser(subparsers)

    args = parser.parse_args()

    if args.refresh_cache:
        refresh_cache(args.refresh_cache)

    args.func(args)


def refresh_cache(path: str):
    playlist_data = playlist_songs_from_api("be_cracked")
    save_playlist_data(path, playlist_data)


if __name__ == '__main__':
    main()
