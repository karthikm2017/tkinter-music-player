#!/usr/bin/env python3


import os
import threading
import time
from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3

from tkinter import *
import tkinter.messagebox
from pygame import mixer
from tkinter import filedialog

root = tk.ThemedTk()
root.get_themes()
root.set_theme("breeze")

statusbar = ttk.Label(root, text='WELCOME TO MUSIC PLAYER- BY KARTHIK', relief=SUNKEN, anchor=W,
                      font='Times 10  italic')
statusbar.pack(side=BOTTOM, fill=X)

# create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the sub menu
subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the file name
# fullpath + filename is requred to play the music under play_music load function


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo(' about music player', 'this is a music player')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About us", command=about_us)

mixer.init()  # initializing the mixer

# to add the icon of the app this is used not root.iconbitmap function it will not work
root.title("music player")
p1 = PhotoImage(file='images/music-work.png')
root.iconphoto(False, p1)

# Root window = Status bar, Left frame, Right frame
# left frame = listbox(playlist)
# right frame = topframe,middleframe,and bottom frame


leftfraame = Frame(root)
leftfraame.pack(side=LEFT, padx=30, )

playlistbox = Listbox(leftfraame)
playlistbox.pack()

addbtn = ttk.Button(leftfraame, text='+ Add', command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


deletebtn = ttk.Button(leftfraame, text='- Delete', command=del_song)
deletebtn.pack(side=LEFT)

rightfraame = Frame(root)
rightfraame.pack(pady=10)

topframe = Frame(rightfraame)
topframe.pack()

lengthlable = ttk.Label(topframe, text='Total Length : --:--', )
lengthlable.pack(pady=5)

currenttimelable = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelable.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div = total_length/60, mod = total_length%60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformate = '{:02d}:{:02d}'.format(mins, secs)
    lengthlable['text'] = "Total Length" + ' - ' + timeformate
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy() :  returns false when we press the stop button (music stops playing)
    # continue ignores all of the statement below it , we check if music is paused or not
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:

            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformate = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelable['text'] = "Current Time" + ' ' + timeformate
            time.sleep(1)
            current_time += 1


def play_music():
    global paused
    if paused:
        mixer.music.unpause()  # if initialised goes to the else condition
        statusbar['text'] = "Music resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "playing music" + ' ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror("File not found", "Music player couldn't open this type of file")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "music stoped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "music paused"


def rewind_music():
    play_music()
    statusbar['text'] = "music rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes only values from 0 to 1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.3)
        VolumeBtn.config(image=VolumePhoto)
        scale.set(30)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        VolumeBtn.config(image=MutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightfraame)
middleframe.pack(pady=30, padx=30)

PlayPhoto = PhotoImage(file='images/play.png')
PlayBtn = ttk.Button(middleframe, image=PlayPhoto, command=play_music)
PlayBtn.grid(row=0, column=0, padx=10)

StopPhoto = PhotoImage(file='images/stop.png')
StopBtn = ttk.Button(middleframe, image=StopPhoto, command=stop_music)
StopBtn.grid(row=0, column=1, padx=10)

PausePhoto = PhotoImage(file='images/pause.png')
PauseBtn = ttk.Button(middleframe, image=PausePhoto, command=pause_music)
PauseBtn.grid(row=0, column=2, padx=10)

# bottomframe for volume mute rewind button etc....

bottomframe = Frame(rightfraame)
bottomframe.pack()

RewindPhoto = PhotoImage(file='images/rewind.png')
RewindBtn = ttk.Button(bottomframe, image=RewindPhoto, command=rewind_music)
RewindBtn.grid(row=0, column=0)

MutePhoto = PhotoImage(file='images/mute.png')
VolumePhoto = PhotoImage(file='images/volume.png')
VolumeBtn = ttk.Button(bottomframe, image=VolumePhoto, command=mute_music)
VolumeBtn.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(30)  # implement the default volume
mixer.music.set_volume(0.3)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_close():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
