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
    scope="user-library-read playlist-modify-private playlist-read-private playlist-read-collaborative"
))

def get_existing_playlists():
    existing = {}
    results = sp.current_user_playlists()

    while results:
        for playlist in results['items']:
            existing[playlist['id']] = playlist['name']

        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return existing

def delete_api(user_playlists_dict):
    current_user_id = sp.current_user()['id']
    for id, name in user_playlists_dict.items():        
        if name.startswith("[Spotify API]"):
            print(f"Deleting: {name}")
            sp.user_playlist_unfollow(current_user_id, id)


user_playlists = get_existing_playlists()
delete_api(user_playlists)