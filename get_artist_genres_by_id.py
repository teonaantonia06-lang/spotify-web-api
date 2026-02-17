# CAREFUL
# this will need to be modified in order to take songs from UNORGANIZED, instead of liked songs

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

def get_genres(artist_id):
    genres = {}
    artist = sp.artist(artist_id)
    genres = artist['genres']
    return genres

# CHANGE THIS WITH THE ID OF THE DESIRED ARTIST
searched_artist_id = "4ZgQDCtRqZlhLswVS6MHN4"

searched_genres = get_genres(searched_artist_id)
print(searched_genres)