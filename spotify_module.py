import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import creditentials as cred
import os
import time
from dotenv import load_dotenv

# Dokumentacja
# https://spotipy.readthedocs.io/en/master/#examples

# dokumentacja odnośnie metody search:
# https://developer.spotify.com/documentation/web-api/reference/#/operations/search

# Odnośnie type:
# array
# required
#
# A comma-separated list of item types to search across. Search results include hits from all the specified item types. For example: q=abacab&type=album,track returns both albums and tracks matching "abacab".
# Allowed values:"album""artist""playlist""track""show""episode"
# Example value:"track,artist"

# Available vs active device:
# https://github.com/Peter-Schorn/SpotifyAPI/wiki/Using-the-Player-Endpoints

load_dotenv() # enables access to environment variables
scope = "user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('client_id'), client_secret=os.environ.get('client_secret'),
                                                    redirect_uri=os.environ.get('redirect_url'), scope=scope))


def get_device_id():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                        redirect_uri=cred.redirect_url, scope=scope))
    id = spotify.devices()['devices'][0]['id']
    return id


def play_song(song_name):
    spotify_app_location = r'C:/Users/pawni/AppData/Roaming/Spotify/Spotify.exe'
    os.popen(spotify_app_location)
    time.sleep(2)
    x = spotify.search(f'{song_name}', limit=1, offset=0, type="track")
    the_track = x['tracks']['items'][0]['uri']
    try:
        spotify.start_playback(device_id=get_device_id(), uris=[the_track])
    except Exception as e:
        print(e)


def pause_song():
    spotify.pause_playback(device_id=get_device_id())


def resume_song():
    spotify.start_playback(device_id=get_device_id())


def next_song():
    spotify.next_track(device_id=get_device_id())


def previous_song():
    spotify.previous_track(device_id=get_device_id())


def change_volume(value):
    current_volume = int(spotify.devices()['devices'][0]['volume_percent'])
    spotify.volume((current_volume + value), get_device_id())


def get_playlists():
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                                        redirect_uri=cred.redirect_url, scope=scope))
    playlists_dict = {}
    user_playlists = spotify.user_playlists(user='ogtjlxt7qt9uyeny71thmrgu7')
    playlists_raw = user_playlists['items']
    for playlist in playlists_raw:
        key = playlist['name']
        value = playlist['uri']
        playlists_dict[key] = value

    return playlists_dict


def select_playlist(playlist_uri):
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(client_id=os.environ.get('client_id'), client_secret=os.environ.get('client_secret'),
                                  redirect_uri=os.environ.get('redirect_url'), scope=scope))
    try:
        spotify_app_location = r'C:/Users/pawni/AppData/Roaming/Spotify/Spotify.exe'
        os.popen(spotify_app_location)
        time.sleep(3)
        spotify.start_playback(device_id=get_device_id(), context_uri=playlist_uri)
    except Exception as e:
        print(e)



# scopes = [
#     "user-read-email",
#     "playlist-read-private",
#     "playlist-read-collaborative",
#     "user-read-email",
#     "streaming",
#     "user-read-private",
#     "user-library-read",
#     "user-top-read",
#     "user-library-modify",
#     "user-read-playback-state",
#     "user-modify-playback-state",
#     "user-read-currently-playing",
#     "user-read-recently-played",
#     "user-read-playback-state",
#     "user-follow-read"
# ]
