# Clustify

This project is mostly me playing around with the Spotify API, creating a usable CLI, and hone some of my python skills.

## Motivation
The main problem clustify is trying to solve is that I sometimes have a song but am not quite sure in which of my playlists to put it.

## How it works
So to find a way to suggest a playlist for a song or simply explore related music I listen to, I consider playlists as clusters by taking the average values of spotify's audio features for each song in the playlist.
Then I can calculate the distance between the song and each playlist and sort them by their distance.
This sometimes gives very interesting and surprising results. I have polished the CLI so far that one can easily list their most similar playlists for any given (or the currently playing) song.

There is a lot that can still be done to improve the results, such as
- using a different distance metric
- considering only some audio features or weigh them in some way
- comparing playlists
- ...

## Usage

NOTE: If you did not build the Clustify app substitute `Clustify` with `poetry run python src/clustify/run.py` in the following commands.

On the first run you need to execute `Clustify --refresh_cache --user <username>` to cache the metadata and audio features of your playlists.
Ensure the environment variables for Spotipy are set correctly.
This includes the `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET` and `SPOTIPY_REDIRECT_URI` variables (see [spotipy docs](https://spotipy.readthedocs.io/en/2.22.0/?highlight=URI#authorization-code-flow)).
`SPOTIPY_REDIRECT_URI` should be set to `http://localhost:8080/` for the app-user authentication.
A browser window will open and you need to copy the url you are redirected to into the terminal.

Then you can run the `song_distance` routine with `Clustify song_distance` to get a list of the most similar playlist for the currently playing song.

An example output would be:
```
$ clustify song_distance "https://open.spotify.com/track/3z8h0TU7ReDPLIbEnYhWZb?si=57e5e9e21455418d"
Song: Bohemian Rhapsody - Queen
[('Esstresso', 0.716),
 ('парить', 0.781),
 ('Gittaren Nostalgie', 0.786),
 ('Thrown Back Too Far', 0.802),
 ('Sans', 0.807),
 ('Grüne Nostalgie', 0.808),
 ('Я не понимаю', 0.812)]
```

Lower number means the song is "closer" to the playlist.

You can also check for a specific song by its id with `Clustify song_distance <song_id>`.
E.g., `Clustify song_distance "https://open.spotify.com/track/4u7EnebtmKWzUH433cf5Qv?si=90b17bda87184889"`.

## Dev Quickstart
### Python
Uses poetry for environment management.
Run `poetry install` to install the virtual environment.

### Spotipy
Ensure the three environment variables required for app-user authentication are set (see [Usage](#usage)).

### Building
This step is optional.

Ensure you have `pyinstaller` in your poetry venv (run `poetry install --with build`).
Then run `build.sh` and the finished executable for your OS can be found in the `dist` folder.

### Installation

Under linux you can make clustify executable from everywhere for you current user by linking it to `~/.local/bin` with ```ln -s `pwd`/dist/clustify ~/.local/bin/clustify```.
For this to work you need to have your spotipy environment variables set globally, i.g. in your `.bashrc` or `.zshrc` file.

_Alternatively_, you create the `.env` file in this project and use the `run.sh` script to run clustify.
The `run.sh` script is created by `build.sh` script and can be used to run clustify from anywhere.
Fot this only the `.env` file must be created in the project directory, which contains the secret environment variables.
The `env` file should look like this:
```
SPOTIPY_CLIENT_ID=<your_client_id>
SPOTIPY_CLIENT_SECRET=<your_client_secret>
SPOTIPY_REDIRECT_URI=http://localhost:8080/
```
The link command for this is ```ln -s `pwd`/run.sh ~/.local/bin/clustify```.

NOTE: The `run.sh` script is a quite hacky solution and might not work for everyone. During build time the current working directory is hardcoded into the script. If you move the project folder after building, the script will not work anymore.
