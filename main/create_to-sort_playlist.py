from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read playlist-modify-private"
))

def get_all_liked_songs():
    all_tracks = []
    results = sp.current_user_saved_tracks(limit=50)

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                all_tracks.append(track['id'])

        if results['next']:
            results = sp.next(results)
        else:
            break
    return all_tracks

def already_sorted_to_set(playlist_id):
    sorted_set = set()
    results = sp.playlist_items(playlist_id)

    while results:
        for item in results['items']:
            if item['track']:
                track_id = item['track']['id']
                if track_id:
                    sorted_set.add(track_id)
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return sorted_set

def create_to_sort_list(all, sorted):
    to_sort_list = []
    for song in all:
        if song not in sorted:
            to_sort_list.append(song)
    return to_sort_list

def add_to_playlist(tracks, playlist_id):
    for i in range(0, len(tracks), 100):
        batch = tracks[i : i + 100]
        sp.playlist_add_items(playlist_id, batch)
        print(f"  - Added {len(batch)} tracks...")


liked_tracks = get_all_liked_songs()

# CAREFUL HERE 
already_sorted_playlist_id = "3AfbSXqo5F0aN2qgYHc6w0"
to_sort_playlist_id = "6MeBiKxo4qWhBdO5NSZmoN"

already_sorted_set = already_sorted_to_set(already_sorted_playlist_id)

to_sort_tracks = create_to_sort_list(liked_tracks, already_sorted_set)

add_to_playlist(to_sort_tracks, to_sort_playlist_id)


