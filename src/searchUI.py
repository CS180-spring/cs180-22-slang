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

library_df = pd.read_csv("../library/big_library.csv",low_memory=False)
library_df['track_name'] = library_df['track_name'].astype(str)
library_df['artist'] = library_df['artist'].astype(str)
library_df['album'] = library_df['album'].astype(str)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_rows', 20)


def advanced_search(library_df, songTitle, artist, album, songID, danceability, energy, loudness, speechiness, instrumentalness, liveness):

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

    if songTitle != '' and songTitle != 'Song Title':
        songTitleResult = library_df.loc[library_df["track_name"].str.contains(songTitle, case=False).fillna(False)]
    
    if artist != '' and artist != 'Artist':
        artistResult = library_df.loc[library_df["artist"].str.contains(artist, case=False).fillna(False)]

    if album != '' and album != 'Album':
        albumResult = library_df.loc[library_df["album"].str.contains(album, case=False).fillna(False)]

    if songID != '' and songID != 'Song ID':
        songIDResult = library_df.loc[library_df["track_id"].str.contains(songID, case=False).fillna(False)]

    if danceability != '' and danceability != 'Danceability':
        danceabilityResult = library_df.loc[library_df["danceability"].astype(str).str.contains(danceability, case=False).fillna(False)]
    
    if energy != '' and energy != 'Energy':
        energyResult = library_df.loc[library_df["energy"].astype(str).str.contains(energy, case=False).fillna(False)]

    if loudness != '' and loudness != 'Loudness':
        loudnessResult = library_df.loc[library_df["loudness"].astype(str).str.contains(loudness, case=False).fillna(False)]

    if speechiness != '' and speechiness != 'Speechiness':
        speechinessResult = library_df.loc[library_df["speechiness"].astype(str).str.contains(speechiness, case=False).fillna(False)]

    if instrumentalness != '' and instrumentalness != 'Instrumentalness':
        instrumentalnessResult = library_df.loc[library_df["instrumentalness"].astype(str).str.contains(instrumentalness, case=False).fillna(False)]

    if liveness != '' and liveness != 'Liveness':
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

    playlist_loc = "../output/searchResults.csv"
    results.to_csv(playlist_loc, index = False)




def searchbyTitle(library_df, titleSearch):
    songResult = library_df.loc[library_df['track_name'].fillna('').str.contains(titleSearch, case=False)]

    if not songResult.empty:
        print("Related Songs:")
        songs = songResult[["track_name"]].to_numpy()
        csvName = "../output/" + "cacheSearch" + ".csv"
        songResult.to_csv(csvName, index = False)
    else:
        print("No matching songs found")

def searchbyArtist(library_df, artistSearch):
    artistResult = library_df.loc[library_df['artist'].fillna('').str.contains(artistSearch, case=False)]
    if not artistResult.empty:
        artists = artistResult[["artist"]].drop_duplicates().to_numpy()
        csvName = "../output/" + "searchResults" + ".csv"
        artistResult.to_csv(csvName, index = False)

    else: 
        print("No matching artists found")          

