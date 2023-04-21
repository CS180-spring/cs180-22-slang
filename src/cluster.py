import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

cid = 'ce0010be0c7946a0b9f926585bc24c62'
secret = 'e0d800c29a704893b6ce87886e3b02b8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def extract_playlist_id_from_url(url):
    playlist_id = url.split('/')[-1]
    return playlist_id

def make_playlist_df(creator, playlist_id):
    
    #Making empy dataframe
    attributes_list = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"]
    playlist_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    
    #Loop through playlist
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for song in playlist:
        song_features = {}
        #Get metadata
        song_features["artist"] = song["track"]["album"]["artists"][0]["name"]
        song_features["album"] = song["track"]["album"]["name"]
        song_features["track_name"] = song["track"]["name"]
        song_features["track_id"] = song["track"]["id"]
        
        #Get audio features
        audio_features = sp.audio_features(song_features["track_id"])[0]
        for feature in attributes_list[4:]:
            song_features[feature] = audio_features[feature]
        
        #Combine all the dfs we made in each iteration
        song_df = pd.DataFrame(song_features, index = [0])
        playlist_df = pd.concat([playlist_df, song_df], ignore_index = True)
        
    return playlist_df

inp = input("Please enter link to second playlist: ")
id = extract_playlist_id_from_url(inp)

df2 = make_playlist_df("spotify", id)
df2.to_csv('../output/Playlist2.csv', index = False, header = False)