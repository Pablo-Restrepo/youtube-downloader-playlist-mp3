"""
YouTube Playlist Downloader and Video to MP3 Converter.
This script downloads videos from a YouTube playlist and converts them to MP3 format.
"""

import os
from pytube import Playlist
from moviepy.editor import VideoFileClip


# Directory where files will be saved.
OUTPUT_DIRECTORY = "music"


def delete_mp4_files(directory: str) -> None:
    """
    Delete all .mp4 files in the specified directory.

    Args:
        directory (str): The directory path.
    """
    for file in os.listdir(directory):
        if file.endswith(".mp4"):
            os.remove(os.path.join(directory, file))


def convert_to_mp3(filename: str) -> None:
    """
    Convert a video file to MP3 format.

    Args:
        filename (str): The name of the video file.
    """
    clip = VideoFileClip(filename)
    mp3_filename = filename[:-4] + ".mp3"
    clip.audio.write_audiofile(mp3_filename)
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

            video.streams.get_highest_resolution().download(OUTPUT_DIRECTORY)
            convert_to_mp3(OUTPUT_DIRECTORY + '/' + video.title + ".mp4")
            os.remove(os.path.join(OUTPUT_DIRECTORY, video.title + ".mp4"))

            print("Downloaded: " + video.title)
        except Exception as e:
            print("Error: " + str(e))

    delete_mp4_files(OUTPUT_DIRECTORY)


if __name__ == "__main__":
    main()
