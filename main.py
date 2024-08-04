"""
YouTube Playlist Downloader and Video to MP3 Converter.
This script downloads videos from a YouTube playlist and converts them to MP3 format.
"""

import os
from pytubefix import Playlist
from moviepy.editor import VideoFileClip


class YouTubePlaylistDownloader:
    """
    A class to download videos from a YouTube playlist and convert them to MP3 format.

    Attributes:
        output_directory (str): The directory where the downloaded videos are saved.
    """

    def __init__(self, output_directory="music"):
        self.output_directory = output_directory

    @staticmethod
    def __remove_slashes(string: str) -> str:
        """
        Remove slashes from a string.

        Args:
            string (str): The input string.

        Returns:
            str: The string without slashes.
        """
        string = string.replace("/", "")
        string = string.replace("|", "")
        string = string.replace("\"", "")
        string = string.replace("-", "")
        string = string.replace(",", "")
        string = string.replace(".", "")
        string = string.replace("ñ", "n")
        string = string.replace("Ñ", "N")

        return string

    def __delete_mp4_files(self, directory: str) -> None:
        """
        Delete all .mp4 files in the specified directory.

        Args:
            directory (str): The directory path.
        """
        for file in os.listdir(directory):
            if file.endswith(".mp4"):
                os.remove(os.path.join(directory, file))

    def __convert_to_mp3(self, filename: str) -> None:
        """
        Convert a video file to MP3 format.

        Args:
            filename (str): The name of the video file.
        """
        clip = VideoFileClip(filename)
        mp3_filename = filename[:-4] + ".mp3"
        clip.audio.write_audiofile(mp3_filename)
        clip.close()

    def download_playlist(self, playlist_url: str) -> None:
        """
        Download videos from a YouTube playlist and convert them to MP3 format.

        Args:
            playlist_url (str): The URL of the YouTube playlist.
        """
        playlist = Playlist(playlist_url)

        for video in playlist.videos:
            try:
                video.title = self.__remove_slashes(video.title)
                print("Downloading: " + video.title)

                if not video.streams.get_highest_resolution().download(self.output_directory):
                    print("Error: Unable to download " + video.title)
                    continue

                self.__convert_to_mp3(os.path.join(
                    self.output_directory, video.title + ".mp4"))
                os.remove(os.path.join(
                    self.output_directory, video.title + ".mp4"))

                print("Downloaded: " + video.title)
            except Exception as e:
                print("Error: " + str(e))

        self.__delete_mp4_files(self.output_directory)


if __name__ == "__main__":
    downloader = YouTubePlaylistDownloader()
    play_list_url = input("Enter the playlist url: ")
    downloader.download_playlist(play_list_url)
