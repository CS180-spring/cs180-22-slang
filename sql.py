import sqlite3
import csv
import sys
import pandas as pd 

try: 
    connection = sqlite3.connect('spoti.db')
    cursor = connection.cursor()
    print('SpotiDB')
    
    cursor.execute('''DROP TABLE IF EXISTS test''')
    cursor.execute('''CREATE TABLE test (artist TEXT, album TEXT, song TEXT, songID TEXT)''')

    file = open('smalltest.csv')
    contents = csv.reader(file)
    insert_records = "INSERT INTO test (artist, album, song, songID) VALUES (?, ?, ?, ?)"
    cursor.executemany(insert_records, contents)

    # print('Select what you would like to search by')
    # print('\t1. artist name')
    # print('\t2. album name')
    # print('\t3. song name')
    # search_type = input('Enter choice: ')

    # if search_type == '1': 
    #     search_artist_name = input('Enter artist name: ')
    #     cursor.execute('''SELECT * FROM test WHERE artist = ?''', (search_artist_name,))
    # elif search_type == '2': 
    #     search_album_name = input('Enter album name: ')
    #     cursor.execute('''SELECT * FROM test WHERE album = ?''', (search_album_name,))
    # elif search_type == '3': 
    #     search_song_name = input('Enter song name: ')
    #     cursor.execute('''SELECT * FROM test WHERE song = ?''', (search_song_name,))
    # else: 
    #     print('invalid search type')
    #     sys.exit()

    search_val = input('Enter search keywords: ')
    query = f"SELECT * FROM test WHERE artist LIKE '%{search_val}%' OR album LIKE '%{search_val}%' OR song LIKE '%{search_val}%'"
    cursor.execute(query)

    
    for row in cursor: 
        print(row)
    

except sqlite3.Error as error:
    print('Error occurred - ', error)

finally: 
    if connection: 
        connection.close()
        print('connection closed')