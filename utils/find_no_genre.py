# this will add songs without a listed genre from liked songs to a designated playlist, WITHOUT adding dupplicates

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

            track_info = {
                "name": track['name'],
                "track_id": track['id'],
                "artist_name": track['artists'][0]['name'],
                "artist_id": track['artists'][0]['id']
            }

            all_tracks.append(track_info)

            # print(f"Fetched: {track_info['name']} by {track_info['artist_name']}")

        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return all_tracks

def get_artist_genres(artist_ids):
    # defining a dictionary
    artist_genre_dict = {}

    for i in range(0, len(artist_ids), 50):
        batch = artist_ids[i : i + 50]

        # http get request for Get Several Artists - 50 at a time in this case, because that's the maximum allowed
        results = sp.artists(batch)

        for artist in results['artists']:
            artist_genre_dict[artist['id']] = artist['genres']
    
    return artist_genre_dict

def get_artitsts_without_genres(genre_dict):
    artists_without_genres = set()
    for entry in genre_dict:
        if not genre_dict[entry]:
            artists_without_genres.add(entry)
    return artists_without_genres

# new, tested, should be fine
def get_existing(dest_playlist_id):
    existing_list = []
    results = sp.playlist_items(dest_playlist_id)
    while results:
        for item in results['items']:
            existing_list.append(item['track']['id'])

        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return set(existing_list)

# updated to search, its gonna make it slow
def create_genreless_tracks_list(all_songs, existing, genreless_astists):
    genreless_tracks_list = []
    for song in all_songs:
        if song['artist_id'] in genreless_astists and song['track_id'] not in existing:
            # if find_song_in_playlist(existing, song['track_id']) == 0:
            genreless_tracks_list.append(song['track_id'])

    return genreless_tracks_list

def add_to_playlist(playlist_id, genreless_tracks):
    for i in range(0, len(genreless_tracks), 100):
        batch = genreless_tracks[i : i + 100]
        sp.playlist_add_items(playlist_id, batch)
        print(f"  - Added {len(batch)} tracks...")
    

# careful here
genreless_playlist_id = "1nv0jZcSEbKxhqwOxrVfs7"

all_my_songs = get_all_liked_songs()

unique_artist_ids = list(set([song['artist_id'] for song in all_my_songs]))

master_genre_dict = get_artist_genres(unique_artist_ids)

artists_without_genre = get_artitsts_without_genres(master_genre_dict)

existing = get_existing(genreless_playlist_id)

genreless_tracks = create_genreless_tracks_list(all_my_songs, existing, artists_without_genre)

add_to_playlist(genreless_playlist_id, genreless_tracks)




# lists vs sets
# no need to search in them on your own, python can do that alrdy with in / not in
# the same opperator will have o(n) for lists [], but o(1) on sets {}
# it uses hashing on sets 