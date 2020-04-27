import json
import requests



def song_recommendation(SONG_IDENTIFIER):
    url = f'https://searchly.asuarez.dev/api/v1/similarity/by_song?song_id={SONG_IDENTIFIER}'
    response = requests.get(url).json()
    return response


def main():
    print(song_recommendation('love story'))




if __name__ == "__main__":
    main()

