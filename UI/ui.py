##just run this file to start the UI
import tkinter as tk
from tkinter import ttk
import csv
import os

def load_playlist():
    file_path = os.path.join(os.pardir, 'Playlist1.csv')

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        playlist = list(reader)
        print(playlist)

        treeview1.delete(*treeview1.get_children())

        for row in playlist:
            treeview1.insert("", "end", values=row)


root = tk.Tk()
root.title("SpotiDB")
root.resizable(width=False, height=False)


style = ttk.Style(root)
root.tk.call("source", "./forest-light.tcl")
root.tk.call("source", "./forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

leftFrame = ttk.Frame(frame)
leftFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

#############################
widgets_frame = ttk.LabelFrame(leftFrame, text="Search Database",padding=(20, 10))
widgets_frame.grid(row=0, column=0, padx=20, pady=20, sticky="new")

searchTitle_entry = ttk.Entry(widgets_frame)
searchTitle_entry.insert(0, "Song Title")
searchTitle_entry.bind("<FocusIn>", lambda e: searchTitle_entry.delete('0', 'end'))
searchTitle_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nsew")


searchArtist_entry = ttk.Entry(widgets_frame)
searchArtist_entry.insert(0, "Artist")
searchArtist_entry.bind("<FocusIn>", lambda e: searchArtist_entry.delete('0', 'end'))
searchArtist_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")

loadButton = ttk.Button(widgets_frame, text="Search", style="Accent.TButton")
loadButton.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")

#############################

widgets2_frame = ttk.LabelFrame(leftFrame, text="Paste Playlists",padding=(20, 10))
widgets2_frame.grid(row=1, column=0, padx=20,sticky="new")

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
rightFrame = ttk.Frame(frame)
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

NotebookPlaylist = ttk.Notebook(rightFrame)
NotebookPlaylist.grid(row=1, column=0, padx=(0,20), pady=20, sticky="nsew")

playlistFrame1 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)
playlistFrame2 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)
playlistFrame3 = ttk.LabelFrame(NotebookPlaylist, width=200, height=200)


cols = ("Name", "Age", "Subscription", "Employment")
treeview1 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
treeview1.column("Name", width=100)
treeview1.column("Age", width=50)
treeview1.column("Subscription", width=100)
treeview1.column("Employment", width=100)
treeview1.pack(fill="both", expand=True, side="left")

treeview2 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
treeview2.column("Name", width=100)
treeview2.column("Age", width=50)
treeview2.column("Subscription", width=100)
treeview2.column("Employment", width=100)
treeview2.pack(fill="both", expand=True, side="left")

treeview3 = ttk.Treeview(NotebookPlaylist, show="headings", columns=cols, height=13)
treeview3.column("Name", width=100)
treeview3.column("Age", width=50)
treeview3.column("Subscription", width=100)
treeview3.column("Employment", width=100)
treeview2.pack(fill="both", expand=True, side="left")

scrollbar1 = ttk.Scrollbar(treeview1, orient="vertical", command=treeview1.yview)
scrollbar1.pack(side="right", fill="y")
treeview1.configure(yscrollcommand=scrollbar1.set)

NotebookPlaylist.add(treeview1, text="Playlist 1")
NotebookPlaylist.add(treeview2, text="Playlist 2")
NotebookPlaylist.add(treeview3, text="New Playlist")

#############################

root.mainloop()
load_playlist()
