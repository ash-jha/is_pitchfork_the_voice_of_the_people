import sys
import spotipy
import pandas as pd
import requests
import json
from spotipy.oauth2 import SpotifyClientCredentials

# Usage: python fetch_album_play_counts.py [spotify_api_key.csv] artist_title.csv [output_csv_path]

def main():

    secret_file = sys.argv[1]
    artist_title_file = sys.argv[2]
    output_csv_path = sys.argv[3]

    print('Usage: python fetch_album_play_counts.py [spotify_api_key.csv] [artist_title_csv_path] [output_csv_path]')

    spotify_api_obj = auth_spotify(secret_file)
    artist_title = pd.read_csv(artist_title_file)
    streams_df = generate_play_counts_df(spotify_api_obj,artist_title)
    streams_df.to_csv(output_csv_path)

def auth_spotify(secret_file):
    with open(secret_file) as fhandle:
        secrets = fhandle.read().strip()

    cred = secrets.split(', ')

    client_credentials_manager = SpotifyClientCredentials(client_id=cred[0], client_secret=cred[1])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp


# Check the first 10 results for matching artist name.
# If album name does not match, we abort
# If album name matches but artist name does not match, we assume the first entry is correct.
def get_spotify_album_id(spotify_api,query_artist_name,query_album_name,DEBUG=False):
    # recommended search query is 'artist name + album name'
    search_query = query_artist_name.strip()+' '+query_album_name.strip()

    try:
        album_search_results = spotify_api.search(q=search_query, type='album', limit=10)
        if len(album_search_results['albums']['items']) == 0:
            return None  # Nothing was found
    except Exception as e:
        print(e) # unlikely to happen unless input search query is empty
        print(f'Search Query: {query_artist_name} {query_album_name}')
        return None # log which albums were discarded?

    # If search returns at least one result, loop through to find the first occurence of matching album name and artist
    album_id = None
    for result in album_search_results['albums']['items']:
        album_name = result['name']
        all_artists = ', '.join([people['name'] for people in result['artists']]).lower()  # should match pitchfork data
        album_artist = all_artists.strip()

        if album_name != query_album_name and album_artist != query_artist_name:
            continue # skip if album name and artist name does not match

        album_uri = result['uri']
        album_id = album_uri.split(':')[2]

        # If the current loop reaches this point, we have found the correct album id.
        break

    return album_id # if loop did not break, this will return None


def get_album_play_count(album_id):
    api_url = 'https://t4ils.dev:4433/api/beta/albumPlayCount?albumid='+album_id  # this url might break in the future

    play_count_json = requests.get(api_url).text

    play_count = json.loads(play_count_json)
    album_agg_count = 0

    for track in play_count['data']:
        try:
            album_agg_count += track['playcount']
        except Exception as e:
            print(e)
            print('Error occured for the following data:')
            print(track)
            print(f'Something wrong with album id: {album_id}')

    return album_agg_count


def generate_play_counts_df(spotify_api,artist_title_df):
    streams_df = pd.DataFrame(columns=['artist', 'title', 'stream_count'])

    for i, row in artist_title_df.iterrows():
        artist_name = row[0]
        album_name = row[1]

        album_id = get_spotify_album_id(spotify_api,artist_name,album_name)

        album_play_count = get_album_play_count(album_id)
        streams_df.loc[i] = [artist_name, album_name, album_play_count]

    return streams_df

if __name__ == '__main__':
    main()