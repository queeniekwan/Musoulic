import json
import requests
from pprint import pprint

def find_lyrics(artist='', song=''):
    artist = artist.replace(' ', '%20')
    song = song.replace(' ', '%20')
    url = f'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={artist}&song={song}'
    response = requests.get(url).json()

    return response

def main():
    lyrics = find_lyrics('james taylor', 'How Sweet It Is (to Be Loved by You)')
    pprint(lyrics)

if __name__ == "__main__":
    main()

