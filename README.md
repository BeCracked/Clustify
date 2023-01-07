# Clustify

## Dev Quickstart
### Python
Uses poetry for environment management.
Run `poetry install` to install the virtual environment.

### Spotipy
Set the three environment variable required for app-user authentication. See 
https://spotipy.readthedocs.io/en/2.22.0/?highlight=URI#authorization-code-flow.

### Execution
To run for example the `song_routine` for a specific song execute `poetry run python src/clustify/run.py song_distance "https://open.spotify.com/track/4u7EnebtmKWzUH433cf5Qv?si=90b17bda87184889"`.

NOTE: Currently you still need to run `poetry run python src/clustify/run.py --refresh_cache song_distance` once to actually load the cache.
This might take a while since it pulls the metadata and audio features for all your playlist. But this needs only to be done once.

### Building
Ensure you have `pyinstaller` in your poetry venv (run `poetry install --with build`).
Then simply run `build.sh` and the finished executable for your OS can be found in the `dist` folder.
