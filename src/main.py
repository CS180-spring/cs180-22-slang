import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd

cid = 'ce0010be0c7946a0b9f926585bc24c62'
secret = 'e0d800c29a704893b6ce87886e3b02b8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def extract_playlist_id_from_url(url):
    playlist_id = url.split('/')[-1]
    return playlist_id

def make_playlist_df1(creator, playlist_id):
    
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

def make_playlist_df2(creator, playlist_id):
    
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

def runKmeans(input_df):
    inp3 = input("Please enter link to second playlist: ")
    id2 = extract_playlist_id_from_url(inp3)
    df2 = make_playlist_df2("spotify", id2)
    df2.to_csv('../output/Playlist2.csv', index = False)

    combined_df = pd.concat([input_df, df2], ignore_index= True)

    #removing duplicates
    combined_df = combined_df.drop_duplicates(subset = ['track_id'], keep = 'first')
    #normalizing values
    x = combined_df.iloc[:, 4:].values 
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    scaled_df = pd.DataFrame(x_scaled)

    kmeans = KMeans(init="k-means++", n_clusters=3, random_state=15, max_iter = 100).fit(x_scaled)
    scaled_df['cluster number'] = kmeans.labels_
    scaled_df.columns = ['danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness', 'cluster number']
    cluster_df = scaled_df.iloc[:, -1:]
    return_df = pd.concat([combined_df, scaled_df], axis=1, join='inner')
    return return_df

inp = input("Please enter link to playlist: ")
id = extract_playlist_id_from_url(inp)

df = make_playlist_df1("spotify", id)
df.to_csv('../output/Playlist.csv', index = False)

inp2 = input("Would you like to merge your playlist with another? Y?N: ")

if inp2 == 'Y':
    combined_df = runKmeans(df)
    combined_df.to_csv('../output/output.csv')