import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import pygal
from pygal.style import Style
from pygal.colors import darken, is_foreground_light, lighten
import copy
from boto.s3.connection import S3Connection


# Get Config Variables 
s3 = S3Connection(os.environ['SPOTIFY_CLIENT_KEY'], os.environ['SPOTIFY_CLIENT_SECRET'])

# Create API object
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_KEY, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_song(query):
    '''
    Search a track with a query (string)
    return the top one searched result 
    return a dict with its song name, song id, artist, artist id, album, and release date
    '''
    r = sp.search(query, type='track', limit=1)
    song = r['tracks']['items'][0]['name']
    song_id = r['tracks']['items'][0]['id']
    artist = r['tracks']['items'][0]['artists'][0]['name']
    artist_id = r['tracks']['items'][0]['artists'][0]['id']
    album = r['tracks']['items'][0]['album']['name']
    release_date = r['tracks']['items'][0]['album']['release_date']
    song_info = {'song': song, 'song_id': song_id, 'artist': artist, 'artist_id': artist_id, 'album': album, 'release_date':release_date}

    return song_info

def song_features(id):
    '''
    returns a dictionary with a track's features, searcing with the track's id
    id is a string
    '''
    r = sp.audio_features([id])

    return r[0]

def features_visualization(features):
    '''
    features - a dictionary of track features
    prints a bar chart of selected features (on the same scale of 0-1)
    '''
    feature_dict = copy.deepcopy(features)
    # exclude some features
    for feature in ['time_signature','mode','loudness', 'key','tempo','duration_ms','analysis_url', 'id', 'track_href', 'type', 'uri']:
        del feature_dict[feature]

    # customize chart style
    custom_style = Style(
        background = 'rgba(253, 247, 246, 0.4)',
        plot_background = 'rgba(249, 228, 225, 1)',
        foreground = 'rgba(0, 0, 0, 0.9)',
        foreground_strong = 'rgba(0, 0, 0, 0.9)',
        foreground_subtle = 'rgba(0, 0, 0, 0.5)',
        opacity = '.6',
        opacity_hover = '.9',
        colors = (
            '#d94e4c', '#e5884f', '#39929a', lighten('#d94e4c', 10),
            darken('#39929a', 15), lighten('#e5884f', 17), darken('#d94e4c', 10),
            '#234547')
        )
    
    # create chart
    chart =  pygal.HorizontalBar(style=custom_style)
    chart.title = 'Track Features'
    for feature, value in feature_dict.items():
        chart.add(feature, value)
    chart.render()

    return chart.render_data_uri()

def key(track_key):
    '''returns the corresponding pitch class (str) from the integer annotation (int) '''

    pitch_class = {0: 'C', 
    1: 'C#, Db', 
    2: 'D', 
    3: 'D#, Eb', 
    4: 'E', 
    5: 'F', 
    6: 'F#, Gb', 
    7: 'G', 
    8: 'G#, Ab', 
    9: 'A', 
    10: 'A#, Bb',
    11: 'B',}

    return pitch_class[track_key]

def mode(track_mode):
    ''' returns the corresponding modality scale (str) from the mode (int 0 or 1) '''
    if track_mode == 1:
        return 'Major'
    elif track_mode == 0:
        return 'Minor'

def emotion(features):
    '''
    returns an emotion tag (string) based on a song's features (dict)
    '''
    emotion = ''
    if features['energy']>=0.7 or features['speechiness']>=0.08 or features['valence']>=0.6:
        emotion = 'Energetic'
    elif features['energy']<0.7 or features['speechiness']<0.08 or features['valence']>0.5:
        emotion = 'Happiness'
    elif features['energy']<0.45 or features['speechiness']<0.035 or features['valence']<0.3:
        emotion = 'Sadness'

    return emotion

def recommendations(song_id='', artist_id=''):
    '''
    return a list of 5 songs recommended based on an seed track, 
    searching with track's id and artist's id
    '''
    r = sp.recommendations(seed_tracks=[song_id], seed_artist=[artist_id], limit=5)
    recom_list = []
    for track in r['tracks']:
        song = track['name']
        artist = track['artists'][0]['name']
        s = f'{song} - {artist}'
        recom_list.append(s)

    return recom_list
    
def main():
    song_info = search_song('love story')
    print(song_info)
    if song_info:
        features = song_features(song_info['song_id'])
        pprint(features)
        rec = recommendations(song_info['song_id'], song_info['artist_id'])
        print(rec)

        features_visualization(features)

if __name__ == "__main__":
    main()

