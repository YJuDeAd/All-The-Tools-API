from pytubefix import YouTube
from pytubefix.cli import on_progress

async def yt_to_mp4(url: str):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_highest_resolution()
    ys.download(output_path="./fileProcessing/")

    return yt.title

async def yt_to_m4a(url: str):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(output_path="./fileProcessing/")
    
    return yt.title