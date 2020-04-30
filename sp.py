''' Instalation and create enviroment

pip3 install spotipy
export SPOTIPY_CLIENT_ID=146abbf4a23e4b4d9ecb410a9923a35f
export SPOTIPY_CLIENT_SECRET=eecbb95959074abb8d773a216294b6b0
'''

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt

client_id = '146abbf4a23e4b4d9ecb410a9923a35f'
client_secret = 'eecbb95959074abb8d773a216294b6b0'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_song(query):
    '''
    Search a track with query (string)
    return the top one searched result 
    return a dict with its song name, song id, artist, artist id, album, and release date
    '''
    r = sp.search(query, type='track', limit=1)
    try:
        song = r['tracks']['items'][0]['name']
        song_id = r['tracks']['items'][0]['id']
        artist = r['tracks']['items'][0]['artists'][0]['name']
        artist_id = r['tracks']['items'][0]['artists'][0]['id']
        album = r['tracks']['items'][0]['album']['name']
        release_date = r['tracks']['items'][0]['album']['release_date']
        song_info = {'song': song, 'song_id': song_id, 'artist': artist, 'artist_id': artist_id, 'album': album, 'release_date':release_date}
    except:
        song_info = {}
    return song_info

def song_features(id):
    '''
    returns a dictionary with a track's features, searcing with the track's id
    id is a string
    '''
    r = sp.audio_features([id])

    return r[0]

def features_visualization(feature_dict):
    '''
    features - a dictionary of track features
    prints a bar plot of all features
    '''
    # exclude some features
    for feature in ['tempo','duration_ms','analysis_url', 'id', 'track_href', 'type', 'uri']:
        del feature_dict[feature]

    # convert scalar values into lists
    for feature, value in feature_dict.items():
        value_list = [value]
        feature_dict[feature] = value_list

    # creat pandas DataFrame and plot bar chart
    df = pd.DataFrame(feature_dict)
    row = df.iloc[0]
    row.plot(kind='bar', x='Features', y='Values', title='Track Features')
    plt.show()


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
    song_info = search_song('cradles sub urban')
    print(song_info)
    if song_info:
        features = song_features(song_info['song_id'])
        pprint(features)
        rec = recommendations(song_info['song_id'], song_info['artist_id'])
        print(rec)
        features_visualization(features)


if __name__ == "__main__":
    main()

