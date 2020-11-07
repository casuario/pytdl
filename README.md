# pytdl
simple tkinter ui for pytube

this is mainly for learning purposes

it uses tkinter and ttkthemes for the GUI and  pytube (currently this version, as it is the most updated   
and error-free i've found: https://github.com/H4KKR/pytubeX)

In order to download adaptive videos (DASH) the user needs to have installed ffmpeg  
(and in windows declared in the path environment variable)  
When downloading and adaptive video, the program will automatically match a compatible audio stream  
with the highest bitrate possible.

For progressive and audio only streams ffmpeg is not needed.

Only tested in windows 10

it works fine with auto py to exe  
(not with the one file option as it cannot find the images in the resources folder)

TODO:

- optimizing imports  
- improving code (remove duplicate, divide in files, cleaner use of variables for file paths ...)  
- implement automatical removal of temp files when downloading DASH streams
- implement some sort of progress feedback when downloading a video
- adjust width of app to make sure all stream info fits in
- test it in linux
