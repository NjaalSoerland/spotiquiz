import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from the .env file
load_dotenv()

# Set up API credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIPY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'],
                                               scope="user-modify-playback-state user-top-read"))


def play_random_song(songs):
    random_song = random.choice(songs)
    devices = sp.devices()
    device_id = devices['devices'][0]['id']
    sp.start_playback(device_id, uris=[random_song['uri']])
    return random_song['name'], random_song['artists']


def get_top_songs(limit=100, time_range='short_term'):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [{'name': item['name'], 'artists': [artist['name'] for artist in item['artists']], 'uri': item['uri']} for item in results['items']]


def main():
    print("Welcome to the Spotify Song Guessing Game!")
    print("Playing a random song from your top 100 songs...")

    top_songs = get_top_songs()
    song_name, artists = play_random_song(top_songs)

    print("Now playing... Guess the name of the song!")
    while True:
        guess = input("Enter your guess: ")
        if guess.lower() == song_name.lower():
            print(
                f"Congratulations! You're right. The song is '{song_name}' by {', '.join(artists)}")
            break
        else:
            print("Incorrect! Try again.")


if __name__ == '__main__':
    main()
