import numpy
import pandas as pd
import editDist

import itertools

from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown
from rich.text import Text
from rich.progress import Progress
import time

from fuzzywuzzy import fuzz

pd.set_option('display.max_rows', 20)

def search(library_df): 
    print("Search by:")
    print("1. Song name")
    print("2. Artist name")
    print("3. Album name")
    print("4. Quit")
    searchBy = input("Please enter what you would like to search by: ")
    while searchBy != '4':
        if searchBy == '1':
            songSearch = input("Please enter the song name you would like to search for: ")
            songResult = library_df.loc[library_df['track_name'].fillna('').str.contains(songSearch, case=False)]

            if not songResult.empty:
                print("Related Songs:")
                print(songResult[["track_name", "artist", "album"]])
                
                songs = songResult[["track_name"]].to_numpy()
                songToAdd = input("Which song would you like to add: ")
                if songToAdd in songs:
                    return songResult.loc[songResult["track_name"] == songToAdd]
                else: 
                    print("invalid song")
            
            else:
                print("No matching songs found")

        elif searchBy == '2':
            artistSearch = input("Please enter the artist name you would like to search for: ")
            artistResult = library_df.loc[library_df['artist'].fillna('').str.contains(artistSearch, case=False)]



            if not artistResult.empty:
                artists = artistResult[["artist"]].drop_duplicates().to_numpy()

                print("Related Artists:")
                for artist in artists:
                    print(artist)
                
                artistSearch = input("Which artist would you like to see: ")
                if artistSearch in artists:
                    newArtistResult = library_df.loc[library_df["artist"] == artistSearch]
                    print(newArtistResult[["track_name", "album"]])

                    songs = newArtistResult[["track_name"]].to_numpy()
                    songToAdd = input("Which song would you like to add: ")
                    if songToAdd in songs:
                        return artistResult.loc[artistResult["track_name"] == songToAdd]
                    else: 
                        print("invalid song")

                else:
                    print("invalid artist")  

            else: 
                print("No matching artists found")          
            
        elif searchBy == '3':
            albumSearch = input("Please enter the album name you would like to search for: ")
            albumResult = library_df.loc[library_df['album'].fillna('').str.contains(albumSearch, case=False)]

            if not albumResult.empty:
                albums = albumResult[["album", "artist"]].drop_duplicates().to_numpy()

                print("Related albums:")
                for album in albums: 
                    print(album)

                albumSearch = input("Which album would you like to see: ")
                if albumSearch in albums: 
                    newAlbumResult = library_df.loc[library_df["album"] == albumSearch]
                    print(newAlbumResult[["track_name"]])

                    songs = newAlbumResult[["track_name"]].to_numpy()
                    songToAdd = input("Which song would you like to add: ")
                    if songToAdd in songs:
                        return albumResult.loc[albumResult["track_name"] == songToAdd]
                    else: 
                        print("invalid song")

                else: 
                    print("invalid album")

            else:
                print("No matching albums found")

        else: 
            print("Invalid choice")

        print("Search by:")
        print("1. Song name")
        print("2. Artist name")
        print("3. Album name")
        print("4. Quit")
        searchBy = input("Please enter what you would like to search by: ")


def advanced_search(library_df):
    songTitle = input('Enter song title: ')
    artist = input('Enter artist name: ')
    album = input('Enter album name: ')
    songID = input('Enter song ID: ')
    danceability = input('Enter danceability: ')
    energy = input('Enter energy: ')
    loudness = input('Enter loudness: ')
    speechiness = input('Enter speechiness: ')
    instrumentalness = input('Enter instrumentalness: ')
    liveness = input('Enter liveness: ')

    songTitleResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    artistResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    albumResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    songIDResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    danceabilityResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    energyResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    loudnessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    speechinessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    instrumentalnessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])
    livenessResult = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])

    if songTitle != '':
        songTitleResult = library_df.loc[library_df["track_name"].str.contains(songTitle, case=False).fillna(False)]
    
    if artist != '':
        artistResult = library_df.loc[library_df["artist"].str.contains(artist, case=False).fillna(False)]

    if album != '':
        albumResult = library_df.loc[library_df["album"].str.contains(album, case=False).fillna(False)]

    if songID != '':
        songIDResult = library_df.loc[library_df["track_id"].str.contains(songID, case=False).fillna(False)]

    if danceability != '':
        danceabilityResult = library_df.loc[library_df["danceability"].astype(str).str.contains(danceability, case=False).fillna(False)]
    
    if energy != '':
        energyResult = library_df.loc[library_df["energy"].astype(str).str.contains(energy, case=False).fillna(False)]

    if loudness != '':
        loudnessResult = library_df.loc[library_df["loudness"].astype(str).str.contains(loudness, case=False).fillna(False)]

    if speechiness != '':
        speechinessResult = library_df.loc[library_df["speechiness"].astype(str).str.contains(speechiness, case=False).fillna(False)]

    if instrumentalness != '':
        instrumentalnessResult = library_df.loc[library_df["instrumentalness"].astype(str).str.contains(instrumentalness, case=False).fillna(False)]

    if liveness != '':
        livenessResult = library_df.loc[library_df["liveness"].astype(str).str.contains(liveness, case=False).fillna(False)]

    frames = [songTitleResult, artistResult, albumResult, songIDResult, danceabilityResult, energyResult, loudnessResult, speechinessResult, instrumentalnessResult, livenessResult]
    combined = pd.concat(frames) # combined each search table
    
    with Progress() as progress:
        task = progress.add_task("[green]Searching...", total=100)
        while not progress.finished:
            progress.update(task, advance=1)
            # Simulate some delay
            time.sleep(0.1)

    # count how many times a song appears in combined df
    output = {}
    for song in combined.index:
        if song not in output:
            output[song] = 1
        else:
            output[song] += 1

    for index in output:
        if library_df.loc[index, "track_name"].lower() == songTitle.lower() :
            output[index] += 1
        if library_df.loc[index, "artist"].lower() == artist.lower():
            output[index] += 1
        if library_df.loc[index, "album"].lower() == album.lower():
            output[index] += 1
        # songResult = library_df.loc[index, "track_name"]
        # output[index] -= editDist.editDistance(songTitle.lower(), songResult.lower(), len(songTitle), len(songResult))

    # sort by value (number of times song shows up) in reverse
    sorted_output = sorted(output.items(), key=lambda x:x[1], reverse=True)
    converted_dict = dict(sorted_output)

    with Progress() as progress:
        task = progress.add_task("[green]Sorting...", total=100)
        while not progress.finished:
            progress.update(task, advance=1)
            # Simulate some delay
            time.sleep(0.1)

    
    results = pd.DataFrame(columns = ["artist","album","track_name",  "track_id","danceability","energy","loudness", "speechiness","instrumentalness","liveness"])

    # store results in df
    for index in itertools.islice(converted_dict, 20):
        results = pd.concat([results, library_df.loc[[index]]], ignore_index=False)
        # print(library_df.loc[[index]])

    with Progress() as progress:
        task = progress.add_task("[green]Saving as dataframe...", total=100)
        while not progress.finished:
            progress.update(task, advance=1)
            # Simulate some delay
            time.sleep(0.1)

    print(results[["track_name", "artist", "album"]].to_string())



if __name__ == '__main__':
    library_df = pd.read_csv("../library/big_library.csv",low_memory=False)
    library_df['track_name'] = library_df['track_name'].astype(str)
    library_df['artist'] = library_df['artist'].astype(str)
    library_df['album'] = library_df['album'].astype(str)
    advanced_search(library_df)
