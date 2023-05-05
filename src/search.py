import numpy

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
            songResult = library_df.loc[library_df["track_name"].str.contains(songSearch, case=False)]

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
            artistResult = library_df.loc[library_df["artist"].str.contains(artistSearch, case=False)]

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
            albumResult = library_df.loc[library_df["album"].str.contains(albumSearch, case=False)]

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