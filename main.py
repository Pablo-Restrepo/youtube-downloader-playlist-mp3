"""
YouTube Playlist Downloader and Video to MP3 Converter.
This script downloads videos from a YouTube playlist and converts them to MP3 format.
"""

import os
from pytube import Playlist
from moviepy.editor import VideoFileClip


def convert_to_mp3(filename: str) -> None:
    """
    Convert a video file to MP3 format.

    Args:
        filename (str): The name of the video file.
    """
    clip = VideoFileClip(filename)
    clip.audio.write_audiofile(filename[:-4] + ".mp3")
    clip.close()


def main() -> None:
    """
    Main function to download videos from a YouTube playlist and convert them to MP3 format.
    """
    playlist_url = input("Enter the playlist url: ")

    playlist = Playlist(playlist_url)

    for video in playlist.videos:
        try:
            print("Downloading: " + video.title)

            video.streams.get_highest_resolution().download()
            convert_to_mp3(video.title + ".mp4")
            os.remove(video.title + ".mp4")

            print("Downloaded: " + video.title)
        except Exception as e:
            print("Error: " + str(e))


if __name__ == "__main__":
    main()
