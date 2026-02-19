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

# create dict for 
def get_songs_from_playlist(playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']

            track_info = {
                "name": track['name'],
                "track_id": track['id'],
                "artist_name": track['artists'][0]['name'],
                "artist_id": track['artists'][0]['id']
            }

            tracks.append(track_info)

            # print(f"Fetched: {track_info['name']} by {track_info['artist_name']}")

        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return tracks

def get_artist_genres(artist_ids):
    artist_genre_dict = {}

    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i : i + 50]

        results = sp.artists(batch)

        for artist in results['artists']:
            artist_genre_dict[artist['id']] = artist['genres']
    
    return artist_genre_dict

def sort_songs_by_genre(all_songs, genre_dict):
    genre_bins = {}

    for song in all_songs:
        track_id = song['track_id']
        artist_id = song['artist_id']

        genres = genre_dict.get(artist_id, [])

        for genre in genres:
            if genre not in genre_bins:
                genre_bins[genre] = []
            genre_bins[genre].append(track_id)

    return genre_bins

def get_existing_playlists():
    existing = {}
    results = sp.current_user_playlists()

    while results:
        for playlist in results['items']:
            existing[playlist['name']] = playlist['id']

        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return existing

def add_tracks_to_playlist(playlist_id, tracks_ids):
    for i in range(0, len(tracks_ids), 100):
        batch = tracks_ids[i : i + 100]
        sp.playlist_add_items(playlist_id, batch)
        print(f"  - Added {len(batch)} tracks...")

# careful here
playlist_id = "6MeBiKxo4qWhBdO5NSZmoN"

tracks = get_songs_from_playlist(playlist_id)

# Extract unique artist IDs using a set
unique_artist_ids = list(set([song['artist_id'] for song in tracks]))

master_genre_dict = get_artist_genres(unique_artist_ids)

genre_bins = sort_songs_by_genre(tracks, master_genre_dict)

my_playlists = get_existing_playlists()

user_info = sp.current_user()
my_user_id = user_info['id']

print(f"Starting Dry Run for user: {my_user_id}\n")

for genre, tracks in genre_bins.items():
    if not tracks:
        continue

    p_name = f"[Spotify API] {genre}"

    if p_name in my_playlists:
        target_id = my_playlists[p_name]
        print(f"Found existing playlist: {p_name}")
    else:
        new_p = sp.user_playlist_create(user=my_user_id, name=p_name, public=False)
        target_id = new_p['id']
        print(f"Created NEW playlist: {p_name}")

    add_tracks_to_playlist(target_id, tracks)


