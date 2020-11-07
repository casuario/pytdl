import os
import random
import subprocess
import time
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
from functools import partial
from os import path
from pytube import YouTube, StreamQuery
from pytube import exceptions
from ttkthemes import ThemedStyle


def download_selected():
    global error_label
    global stream_type
    global video
    error_label['text'] = ''

    try:
        selected_video = lista_video_streams.get(lista_video_streams.curselection())
        itag = selected_video.split(': ')[1].split(' /')[0]
        dl_video = video_streams.get_by_itag(itag)
        if stream_type.get() == 0:

            audio_adaptive = video.streams.filter(type='audio').filter(subtype=dl_video.subtype).first()
            aleatorio = random.randint(0, 9999999)
            dl_video.download(f'{download_folder}', filename=f'video_temp{aleatorio}')
            audio_adaptive.download(f'{download_folder}', filename=f'audio_temp{aleatorio}')

            while not os.path.exists(f'{download_folder}/video_temp{aleatorio}.{dl_video.subtype}') \
                    or not os.path.exists(f'{download_folder}/audio_temp{aleatorio}.{audio_adaptive.subtype}'):
                time.sleep(1)

            ruta_descarga = f'{download_folder}/{dl_video.title}.{dl_video.subtype}'
            ruta_descarga = ruta_descarga.replace(' ', '_')
            os.system(
                f'ffmpeg -y '
                f'-i {download_folder}/audio_temp{aleatorio}.{audio_adaptive.subtype} '
                f'-i {download_folder}/video_temp{aleatorio}.{dl_video.subtype} -c copy {ruta_descarga}')

        else:
            if os.path.exists(f'{download_folder}/{dl_video.title}.{dl_video.subtype}'):
                os.remove(f'{download_folder}/{dl_video.title}.{dl_video.subtype}')
                dl_video.download(download_folder)
            else:
                dl_video.download(download_folder)

    except tk.TclError:
        error_label['text'] = 'Tienes que seleccionar un stream para poder descargarlo.'


def filter_streams():
    global video_streams
    global video
    if video is not None:
        if stream_type.get() == 2:
            video_streams = video.streams.filter(type='audio').order_by('bitrate').desc()
        elif stream_type.get() == 1:
            video_streams = video.streams.filter(progressive=True, type='video').order_by('resolution').desc()
        else:
            video_streams = video.streams.filter(adaptive=True, type='video').order_by('resolution').desc()
        lista_video_streams.delete(0, tk.END)
        for v in video_streams:
            lista_video_streams.insert(
                tk.END,
                f'ITag: {v.itag} / '
                f'Formato: {v.subtype} / '
                f'Resolución: {v.resolution} / '
                f'Bitrate: {int((v.bitrate / 1000))} kbps / '
                f'Codec: {v.codecs[0]} /'
                f'Tamaño: {int(v.filesize / 1024)} kb')


def search_yt_streams():
    error_label['text'] = ''
    lista_video_streams.delete(0, tk.END)
    global video
    global video_streams
    try:

        video = YouTube(yt_url_entry.get())
        if stream_type.get() == 2:
            video_streams = video.streams.filter(type='audio').order_by('bitrate').desc()
        elif stream_type.get() == 1:
            video_streams = video.streams.filter(progressive=True, type='video').order_by('resolution').desc()
        else:
            video_streams = video.streams.filter(adaptive=True, type='video').order_by('resolution').desc()
        title_label['text'] = video.title
        if len(video_streams) == 0:
            error_label['text'] = 'No se han encontrado streams de ese tipo con esa URL'
        else:

            for v in video_streams:
                lista_video_streams.insert(
                    tk.END,
                    f'ITag: {v.itag} / '
                    f'Formato: {v.subtype} / '
                    f'Resolución: {v.resolution} / '
                    f'Bitrate: {int((v.bitrate / 1000))} kbps / '
                    f'Codec: {v.codecs[0]} /'
                    f'Tamaño: {int(v.filesize / 1024)} kb')

    except exceptions.RegexMatchError:
        error_label['text'] = 'Esa URL es incorrecta'


def select_download_folder(folder):
    global download_folder
    selected_folder = filedialog.askdirectory(initialdir=folder, title='Elige un directorio de descarga')
    if path.isdir(selected_folder):
        download_folder = selected_folder
    chosen_folder_label['text'] = download_folder


video: YouTube
video_streams: StreamQuery
successful_search: bool = False
home_folder: str = path.expanduser('~')
download_folder: str = path.join(home_folder, 'Downloads')

if not path.isdir(download_folder):
    download_folder = home_folder

window = tk.Tk()
window.title('Python Youtube Downloader')
window.iconbitmap('resources/pytdl.ico')
window.geometry('660x480')
window.resizable(False, False)
window.configure(bg='#F5F6F7')

window_style = ThemedStyle(window)
window_style.set_theme('yaru')
# layout all of the main containers

window.grid_columnconfigure(0, weight=1)

# 0 -> adaptive video, 1 -> progressive video, 2 -> audio only
stream_type = tk.IntVar()
stream_type.set(0)
# create all of the main containers

dl_folder_frame = ttk.Frame(window, padding=(10, 25, 5, 10))
dl_folder_frame.grid(row=0, sticky='new')
dl_folder_frame.grid_columnconfigure(2, weight=1)

yt_url_frame = ttk.Frame(window, padding=(10, 5, 5, 10))
yt_url_frame.grid(row=1, sticky='new')
yt_url_frame.grid_columnconfigure(2, weight=1)

radio_frame = ttk.Frame(window, padding=(10, 5, 5, 10))
radio_frame.grid(row=2, sticky='new')
radio_frame.grid_columnconfigure(0, weight=1)
radio_frame.grid_columnconfigure(1, weight=1)
radio_frame.grid_columnconfigure(2, weight=1)

error_frame = ttk.Frame(window, padding=(10, 5, 5, 10))
error_frame.grid(row=3, column=0)
error_frame.columnconfigure(0, weight=1)

title_frame = ttk.Frame(window, padding=(10, 5, 5, 10))
title_frame.grid(row=4, column=0)
title_frame.columnconfigure(0, weight=1)

video_streams_frame = ttk.Frame(window, padding=(10, 5, 5, 10))
video_streams_frame.grid(row=5, column=0)
video_streams_frame.columnconfigure(0, weight=1)

dl_button_frame = ttk.Frame(window, padding=(10, 5, 5, 10))
dl_button_frame.grid(row=6, column=0)
dl_button_frame.columnconfigure(0, weight=1)

dl_folder_icon = tk.PhotoImage(file='resources/dl_folder.png')

directorio_descarga_label = ttk.Label(dl_folder_frame, text='Destino', font='Helvetica 10 bold',
                                      padding=(0, 0, 10, 0))

directorio_descarga_label.grid(row=0, column=0)

chosen_folder_label = ttk.Label(
    dl_folder_frame,
    padding=(10, 0, 0, 0),
    wraplength=300,
    text=download_folder,
    font='Helvetica 10')

chosen_folder_label.grid(row=0, column=1)

folder_image = tk.PhotoImage(file='resources/dl_folder.png')

download_folder_button = ttk.Button(
    dl_folder_frame,
    image=folder_image,
    padding=(5, 0, 3, 0),
    command=partial(select_download_folder, download_folder))

download_folder_button.grid(row=0, column=2, sticky='E')

yt_url_label = ttk.Label(yt_url_frame, text='Url de Youtube', font='Helvetica 10 bold', padding=(0, 0, 10, 0))

yt_url_label.grid(row=1, column=0)

yt_url_entry = ttk.Entry(yt_url_frame, width=75)
yt_url_entry.grid(row=1, column=1)

glass_image = tk.PhotoImage(file='resources/lupa.png')

yt_url_button = ttk.Button(
    yt_url_frame,
    image=glass_image,
    padding=(10, 0, 8, 0),
    command=partial(search_yt_streams))

yt_url_button.grid(row=1, column=2, sticky='E')

radio_adaptive = ttk.Radiobutton(radio_frame, text='Adaptive (Mayor resolución, requiere FFMPEG)', variable=stream_type,
                                 value=0, command=filter_streams)
radio_progressive = ttk.Radiobutton(radio_frame, text='Progressive (Máximo 720p)', variable=stream_type, value=1,
                                    command=filter_streams)
radio_audio = ttk.Radiobutton(radio_frame, text='Solo audio', variable=stream_type, value=2, command=filter_streams)
radio_adaptive.grid(row=2, column=0)
radio_progressive.grid(row=2, column=1)
radio_audio.grid(row=2, column=2)

try:
    subprocess.run(['ffmpeg'], check=True)
except FileNotFoundError:
    radio_adaptive.config(state='disabled')
    stream_type.set(1)
except subprocess.CalledProcessError:
    radio_adaptive.config(state='enabled')

error_label = ttk.Label(
    error_frame,
    font='Helvetica 10 bold',
    text='')

error_label_style = ttk.Style()
error_label_style.configure('Red.TLabel', foreground='red')
error_label.configure(style='Red.TLabel')
error_label.grid(row=3)

title_label = ttk.Label(
    title_frame,
    font='Helvetica 10 bold',
    text='')

title_label.grid(row=4)

lista_video_streams = tk.Listbox(
    video_streams_frame,
    borderwidth=0,
    highlightbackground='#CFD6E6',
    highlightcolor='#CFD6E6',
    width=200
)

lista_video_streams.grid(row=5, column=0)

yscroll = tk.Scrollbar(command=lista_video_streams.yview, orient=tk.VERTICAL)
yscroll.grid(row=5, column=1, sticky='ns')
lista_video_streams.configure(yscrollcommand=yscroll.set)

dl_button = ttk.Button(
    dl_button_frame,
    text='Descargar Seleccionado',
    padding=(10, 5),
    command=partial(download_selected)
)

dl_button.grid(row=6)

window.mainloop()
