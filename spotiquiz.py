import os
import random
import jellyfish
from dotenv import load_dotenv
from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from the .env file
load_dotenv()

# Set up API credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['SPOTIPY_CLIENT_ID'],
                                               client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                                               redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'],
                                               scope="user-modify-playback-state user-top-read user-read-playback-state"))

app = Flask(__name__)

def play_random_song(songs):
    random_song = random.choice(songs)
    devices = sp.devices()
    device_id = devices['devices'][0]['id']
    sp.start_playback(device_id, uris=[random_song['uri']])
    return random_song['name'], random_song['artists']


def get_top_songs(limit=100, time_range='short_term'):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [{'name': item['name'], 'artists': [artist['name'] for artist in item['artists']], 'uri': item['uri']} for item in results['items']]

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    top_songs = get_top_songs()
    global song_name, artists
    song_name, artists = play_random_song(top_songs)
    return {"success": True}

@app.route('/check_guess', methods=['POST'])
def check_guess():
    user_guess = request.form['guess']
    similarity = jellyfish.jaro_winkler(user_guess.lower(), song_name.lower())
    similarity_threshold = 0.85
    if similarity >= similarity_threshold:
        result = {
            "is_correct": True,
            "song_name": song_name,
            "artists": ", ".join(artists)
        }
    else:
        result = {"is_correct": False}
    return result

if __name__ == '__main__':
    app.run(debug=True)