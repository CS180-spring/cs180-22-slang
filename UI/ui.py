##just run this file to start the UI
import tkinter as tk
from tkinter import ttk
import csv
import os

def load_playlist():
    file_path1 = '/Users/ailan/Desktop/Labs/CS180/cs180-22-slang/Playlist.csv'
    file_path2 = '/Users/ailan/Desktop/Labs/CS180/cs180-22-slang/Playlist2.csv'

    with open(file_path1, 'r') as f1:
        reader1 = csv.reader(f1)
        playlist1 = list(reader1)
        print(playlist1)

        treeview1.delete(*treeview1.get_children())

        for row in playlist1:
            treeview1.insert("", "end", values=row)

    with open(file_path2, 'r') as f2:
        reader2 = csv.reader(f2)
        playlist2 = list(reader2)
        print(playlist2)

        treeview2.delete(*treeview2.get_children())

        for row in playlist2:
            treeview2.insert("", "end", values=row)

root = tk.Tk()
root.title("SpotiDB")
root.resizable(width=False, height=False)


style = ttk.Style(root)
script_dir = os.path.dirname(os.path.abspath(__file__))
forest_light_tcl = os.path.join(script_dir, "forest-light.tcl")
forest_dark_tcl = os.path.join(script_dir, "forest-dark.tcl")

root.tk.call("source", forest_light_tcl)
root.tk.call("source", forest_dark_tcl)
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

windowFrameNotebook = ttk.Notebook(frame)
windowFrameNotebook.grid(row=0, column=0)

tab1 = ttk.Frame(windowFrameNotebook)
windowFrameNotebook.add(tab1, text="Tab 1")

tab2 = ttk.Frame(windowFrameNotebook)
windowFrameNotebook.add(tab2, text="Tab 2")

tab3 = ttk.Frame(windowFrameNotebook)
windowFrameNotebook.add(tab3, text="Tab 3")


leftFrame = ttk.Frame(tab1)
leftFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame = ttk.LabelFrame(leftFrame, text="Search Database",padding=(20, 10))
widgets_frame.grid(row=1, column=0, padx=20, pady=20, sticky="new")
searchTitle_entry = ttk.Entry(widgets_frame)
searchTitle_entry.insert(0, "Song Title")
searchTitle_entry.bind("<FocusIn>", lambda e: searchTitle_entry.delete('0', 'end'))
searchTitle_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nsew")


searchArtist_entry = ttk.Entry(widgets_frame)
searchArtist_entry.insert(0, "Artist")
searchArtist_entry.bind("<FocusIn>", lambda e: searchArtist_entry.delete('0', 'end'))
searchArtist_entry.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")
loadButton = ttk.Button(widgets_frame, text="Search", style="Accent.TButton")
loadButton.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="nsew")
#############################

separator = ttk.Separator(leftFrame)
separator.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ew")
#############################

widgets2_frame = ttk.LabelFrame(leftFrame, text="Paste Playlists",padding=(20, 10))
widgets2_frame.grid(row=3, column=0, padx=20, pady=20, sticky="new")
playlist1_entry = ttk.Entry(widgets2_frame)
playlist1_entry.insert(0, "Playlist 1")
playlist1_entry.bind("<FocusIn>", lambda e: playlist1_entry.delete('0', 'end'))
playlist1_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")


playlist2_entry = ttk.Entry(widgets2_frame)
playlist2_entry.insert(0, "Playlist 2")
playlist2_entry.bind("<FocusIn>", lambda e: playlist2_entry.delete('0', 'end'))
playlist2_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

loadButton = ttk.Button(widgets2_frame, text="Load Playlists", style="Accent.TButton", command=load_playlist)
loadButton.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew")


#############################
rightFrame = ttk.Frame(tab1)
rightFrame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
buttonsFrame = ttk.Frame(rightFrame)
buttonsFrame.grid(row=0, column=0, sticky="nsew")

mergeButton = ttk.Button(buttonsFrame, text="Merge", style="Accent.TButton")
mergeButton.grid(row=0, column=0, padx = (0,20),pady=(20,0))

recommendButton = ttk.Button(buttonsFrame, text="Add Recommended", style="Accent.TButton")
recommendButton.grid(row=0, column=1, padx=20,pady=(20,0))

combo_list = ["Sort By", "Title", "Album", "Artist", "Genre", "Release Date"]
combobox = ttk.Combobox(buttonsFrame, state="readonly", values=combo_list)
combobox.current(0)
combobox.grid(row=0, column=2, padx=20,pady=(20,0), sticky="ew")

#############################

separator1 = ttk.Separator(rightFrame)
separator1.grid(row=1, column=0, pady=(20,0), sticky="ew")

############################# 

NotebookPlaylist = ttk.Notebook(rightFrame)
NotebookPlaylist.grid(row=2, column=0, padx=(0,20), pady=20, sticky="nsew")

playlistFrame1 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)
playlistFrame2 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)
playlistFrame3 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)


cols = ("Artist", "Album", "Title", "SongID")
treeview1 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
treeview1.column("Artist", width=100)
treeview1.column("Album", width=100)
treeview1.column("Title", width=100)
treeview1.column("SongID", width=100)
treeview1.pack(fill="both", expand=True, side="left")
for col in cols:
    treeview1.heading(col, text=col)

treeview2 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
treeview2.column("Artist", width=100)
treeview2.column("Album", width=100)
treeview2.column("Title", width=100)
treeview2.column("SongID", width=100)
treeview2.pack(fill="both", expand=True, side="left")
for col in cols:
    treeview2.heading(col, text=col)

treeview3 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
treeview3.column("Artist", width=100)
treeview3.column("Album", width=100)
treeview3.column("Title", width=100)
treeview3.column("SongID", width=100)
treeview3.pack(fill="both", expand=True, side="left")
for col in cols:
    treeview3.heading(col, text=col)


scrollbar1 = ttk.Scrollbar(treeview1, orient="vertical", command=treeview1.yview)
scrollbar1.pack(side="right", fill="y")
treeview1.configure(yscrollcommand=scrollbar1.set)

scrollbar2 = ttk.Scrollbar(treeview2, orient="vertical", command=treeview2.yview)
scrollbar2.pack(side="right", fill="y")
treeview2.configure(yscrollcommand=scrollbar2.set)

scrollbar1_h = ttk.Scrollbar(treeview1, orient="horizontal", command=treeview1.xview)
scrollbar1_h.pack(side="bottom", fill="x")
treeview1.configure(xscrollcommand=scrollbar1_h.set)

scrollbar2_h = ttk.Scrollbar(treeview2, orient="horizontal", command=treeview2.xview)
scrollbar2_h.pack(side="bottom", fill="x")
treeview2.configure(xscrollcommand=scrollbar2_h.set)

NotebookPlaylist.add(treeview1, text="Playlist 1")
NotebookPlaylist.add(treeview2, text="Playlist 2")
NotebookPlaylist.add(treeview3, text="New Playlist")

NotebookPlaylist.add(treeview1, text="Playlist 1")
NotebookPlaylist.add(treeview2, text="Playlist 2")
NotebookPlaylist.add(treeview3, text="New Playlist")

#############################

MiniFrame = ttk.Frame(rightFrame)
MiniFrame.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

###create frame under right frame for buttons

#############################

button1 = ttk.Button(MiniFrame, text="Add", style="Accent.TButton")
button1.grid(row=0, column=0, padx = (40,0),pady=(0,0))

### create button 1 

#############################

button2 = ttk.Button(MiniFrame, text="Delete", style="Accent.TButton")
button2.grid(row=0, column=1, padx = (40,0),pady=(0,0))

### create button 2 

#############################
button3 = ttk.Button(MiniFrame, text="Deselect", style="Accent.TButton")
button3.grid(row=0, column=2, padx = (40,0),pady=(0,0))

### create button 3

#############################

root.mainloop()
load_playlist()
