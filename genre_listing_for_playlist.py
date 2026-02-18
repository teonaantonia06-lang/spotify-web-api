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

# itterate through given playlist 
def create_artist_set(playlist_id):
    artists_set = set()
    results = sp.playlist_items(playlist_id)

    while results:
        for item in results['items']:
            if item['track']:
                artist_id = item['track']['artists'][0]['id']
                if artist_id:
                    artists_set.add(artist_id)
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return artists_set

def get_genres(artist_id):
    artist = sp.artist(artist_id)
    genres = artist['genres']
    if not genres:
        print("Warning: artist " + artist_id + " has no genres!\n")
    return genres

def get_artists_genres(artist_ids):
    genres_set = set()
    for artist in artist_ids:
        single_artist_genres = get_genres(artist)
        genres_set.update(single_artist_genres)
    return genres_set


playlist_id = "63ZVgXPm6YIp7vJBLSqEIP"

artists_id_set = create_artist_set(playlist_id)

genres = get_artists_genres(artists_id_set)

print(genres)
