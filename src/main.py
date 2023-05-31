import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from sklearn.cluster import KMeans
# from sklearn import preprocessing
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown
from rich.text import Text
from rich.progress import Progress
from rich import box
from rich.table import Table
import time
import pandas as pd
from numba import njit,jit,prange
import os
import os.path
import search
import kmeans
import recommend

console = Console(height = 11)
layout = Layout()
cid = 'ce0010be0c7946a0b9f926585bc24c62'
secret = 'e0d800c29a704893b6ce87886e3b02b8'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
@jit(nopython=True)

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

def runKmeans(input_df, input_df2, merged_loc):
    combined_df = kmeans.Classify.run_classification(input_df, input_df2, merged_loc)
    combined_df.to_csv(merged_loc, index = False)

def runRecommend(input_df, lib_df):
    recs = recommend.recommend(input_df, lib_df)
    recs.to_csv("../output/recommendations.csv", index = False)
    return recs


def getPlaylistFromUser(user_spotify_id):
    playlists = sp.user_playlists(user_spotify_id, limit=50)

    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    return playlists
    

library_loc = "../library/library.csv"
library_df = pd.read_csv(library_loc)
library_df['track_name'] = library_df['track_name'].astype(str)
library_df['artist'] = library_df['artist'].astype(str)
library_df['album'] = library_df['album'].astype(str)

# header_text = Text("SpotiDB Terminal", style="bold white")

with Progress() as progress:
    task = progress.add_task("[green]Loading up Terminal Menu...", total=100)
    while not progress.finished:
        progress.update(task, advance=1)
        # Simulate some delay
        time.sleep(0.1)

MARKDOWN = """
# SpotiDB Terminal
"""
md = Markdown(MARKDOWN)
console.print(md) 

title_text = Text("Menu Options", style = "green")

body_content = """
1. Make a new playlist
2. Edit an existing playlist
3. Import a playlist
4. Merge two playlists
5. Get recommendations for a playlist
6. Print Spotify playlists
7. Quit
"""

panel_width = 40
panel_height = 10

body_text = Text(body_content)
body_text.truncate(panel_width * panel_height)

# body_panel = Panel.fit(body_content, title=title_text)
body_panel = Panel(body_content, title=title_text, expand=False, height=11)

layout.split(
    Layout(body_panel)
)

console.print(layout)

# MARKDOWN = """
# # SpotiDB Terminal
# Menu Options

# """
# md = Markdown(MARKDOWN)
# console.print(md) 

# print("1. Make a new playlist")
# print("2. Edit an existing playlist")
# print("3. Import a playlist")
# print("4. Merge two playlists")
# print("5. Get recommendations for a playlist")
# print("6. Print Spotify playlists")
# print("7. Quit")
inp1 = input("Which would you like to do? ")

while inp1 != "7":

    if inp1 == "1":
        playlistExists = True
        while playlistExists:
            newPlaylistName = input("Please name your playlist: ")
            newPlaylist_loc = "../output/" + newPlaylistName + ".csv"
            playlistExists = os.path.isfile(newPlaylist_loc)
            if playlistExists:
                print("Playlist name already exists")
        playlist_df = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
        print("Add songs:")
        inp3 = 'y'
        while inp3.lower() == 'y':
            temp_song = search.advanced_search(library_df, library_loc)
            if not temp_song.empty: 
                if temp_song['track_id'].to_string(index=False) in playlist_df['track_id'].values:
                    inp4 = input("Song already in playlist. Would you still like to add? Y/N: ")
                    if inp4.lower() == "y":
                        print('Song added')
                        playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                else:
                    playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
            inp3 = input("Keep adding songs? Y/N: ")
        playlist_df.to_csv(newPlaylist_loc, index = False)

    elif inp1 == "2":
        playlistExists = False
        while not playlistExists:
            inp2 = input("Please enter the name of the playlist you want to edit: ")
            playlist_loc = "../output/" + inp2 + ".csv"
            playlistExists = os.path.isfile(playlist_loc)
            if not playlistExists:
                print("Playlist does not exist")
        playlist_df = pd.read_csv(playlist_loc)
        print("1. Add song")
        print("2. Remove song")
        inp3 = input("What do you want to do? ")
        if inp3 == "1":
            inp4 = 'y'
            while inp4.lower() == 'y':
                temp_song = search.advanced_search(library_df, library_loc)
                if not temp_song.empty:
                    if temp_song['track_id'].to_string(index=False) in playlist_df['track_id'].values:
                        inp5 = input("Song already in playlist. Would you still like to add? Y/N: ")
                        if inp5.lower() == "y":
                            print('Song added')
                            playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                    else:
                        playlist_df = pd.concat([playlist_df, temp_song], ignore_index= True)
                inp4 = input("Keep adding songs? Y/N: ")
            playlist_df.to_csv(playlist_loc, index = False)
        elif inp3 == "2":
            # Initiate a Table instance to be modified
            table = Table(show_header=True, header_style="green")
            # Modify the table instance to have the data from the DataFrame
            table = search.df_to_table(playlist_df[["track_name", "artist", "album"]], table, index_name='index')
            # Update the style of the table
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            console.print(table)
            inp4 = input("Enter the index of the song you want to remove: ")
            # temp_song = playlist_df.loc[playlist_df[[int(inp4)]]]
            # drop_index = temp_song.index
            playlist_df = playlist_df.drop(int(inp4))
            playlist_df.to_csv(playlist_loc, index = False)

    elif inp1 == "3":
        playlistLink = input("Please enter link to playlist: ")
        id = extract_playlist_id_from_url(playlistLink)
        playlistName = input("Please name your imported playlist: ")

        df = make_playlist_df1("spotify", id)
        csvName = "../output/" + playlistName + ".csv"
        df.to_csv(csvName, index = False)

    elif inp1 == "4":
        playlist1Exists = False
        while not playlist1Exists:
            playlist1 = input("Please enter the first playlist's name: ")
            playlist1_loc = "../output/" + playlist1 + ".csv"
            playlist1Exists = os.path.isfile(playlist1_loc)
            if not playlist1Exists:
                print("Playlist does not exist")

        playlist2Exists = False
        while not playlist2Exists:
            playlist2 = input("Please enter the second playlist's name: ")
            playlist2_loc = "../output/" + playlist2 + ".csv"
            playlist2Exists = os.path.isfile(playlist2_loc)
            if not playlist2Exists:
                print("Playlist does not exist")

        playlistMergeExists = True
        while playlistMergeExists:
            mergedName = input("Please name your new merged playlist: ")
            merged_loc = "../output/" + mergedName + ".csv"
            playlistMergeExists = os.path.isfile(merged_loc)
            if playlistMergeExists:
                print("Playlist name already exist")

        playlist_df1 = pd.read_csv(playlist1_loc)
        playlist_df2 = pd.read_csv(playlist2_loc)

        merged = kmeans.Classify.run_classification(playlist_df1, playlist_df2, merged_loc)
        merged.to_csv(merged_loc, index = False)

    elif inp1 == "5":
        rec_playlist = input("Enter the name of the playlist you want songs recommended for: ")
        playlist_loc = "../output/" + rec_playlist + ".csv"
        playlist_df = pd.read_csv(playlist_loc)
        recommended_songs = runRecommend(playlist_df, library_df)
        playlist_df = pd.concat([playlist_df, recommended_songs], ignore_index=True)
        playlist_df.to_csv(playlist_loc, index=False)

    elif inp1 == "6":
        inp2 = input("Please enter the spotify username: ")
        spotify_playlists = getPlaylistFromUser(inp2)
        inp3 = input("Do you want to import this user's playlists? Y/N: ")
        if inp3.lower() == "y":
            original = []
            changed = []
            
            inp4 = input("Type the index of the playlist you would like to import: ")
            playlist = spotify_playlists['items'][int(inp4)-1]
            id = playlist["uri"].rsplit(":", 1)[-1]
            new_playlist = make_playlist_df1("spotify", id)
            new_name = playlist["name"]
            if " " in new_name:
                new_name = playlist["name"].replace(" ", "_")
                original.append(playlist["name"])
                changed.append(new_name)
            new_loc = "../output/" + new_name + ".csv"
            new_playlist.to_csv(new_loc, index=False)

            # for i, playlist in enumerate(spotify_playlists['items']):
            #     print(i)
            #     id = playlist["uri"].rsplit(":", 1)[-1]
            #     new_playlist = make_playlist_df1("spotify", id)
            #     new_name = playlist["name"]
            #     if " " in new_name:
            #         new_name = playlist["name"].replace(" ", "_")
            #         original.append(playlist["name"])
            #         changed.append(new_name)
            #     new_loc = "../output/" + new_name + ".csv"
            #     new_playlist.to_csv(new_loc, index=False)
            # if original and changed:
            #     renamed = pd.DataFrame({'original name': original, 'new name': changed})
            #     print("The following playlist names were changed to fit our naming conventions:")
            #     print(renamed)
            


    elif inp1 not in ["1", "2", "3", "4", "5", "6", "7"]: 
        print("Not a valid selection")

    # print("1. Make a new playlist")
    # print("2. Edit an existing playlist")
    # print("3. Import a playlist")
    # print("4. Merge two playlists")
    # print("5. Get recommendations for a playlist")
    # print("6. Print Spotify playlists")
    # print("7. Quit")
    console.print(layout)
    inp1 = input("Which do you want to do? ")