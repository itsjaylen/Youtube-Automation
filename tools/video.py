import logging
import os
import re
import urllib.request

import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip
from pytube import YouTube, request

request.default_range_size = 10485760


def process_channel(channel):
    if channel.startswith("https://www.youtube.com/feeds/videos.xml?channel_id="):
        html = requests.get(channel)
        soup = BeautifulSoup(html.text, "xml")
        entry = soup.find("entry")
        link = entry.find("link")

        process_video(link["href"])

    try:
        html = requests.get(channel + "/videos").text
        info = re.search('(?<={"label":").*?(?="})', html).group()
        #date = re.search('\d+ \w+ ago.*seconds ', info).group()
        url = "https://www.youtube.com/watch?v=" + \
            re.search('(?<="videoId":").*?(?=")', html).group()
    except Exception:
        pass

    process_video(url)


def process_video(url):
    blacklisted_chars = ["<", ">", ":", '"', "/",
                         "backslash", "|", "?", "*", ".", ".."]

    video = YouTube(
        url,
        on_complete_callback=None,
        on_progress_callback=None)
    title = video.title

    for char in blacklisted_chars:
        title = title.replace(char, "")

    try:
        video.streams.get_highest_resolution().download(
            f"./videos/{video.author}/{title}")

        with open(f"./videos/{video.author}/{title}/{title}.txt", "a", encoding="utf-8") as f:
            f.truncate(0)
            f.write(f"""
                    Video Title: {title}{video.title}\n
                    Video Upload Date: {video.publish_date}\n
                    Video Description: {video.description}\n
                    Video Views: {video.views}\n
                    Video Length: {round(video.length / 60, 2)} minutes\n
                    """)

            with urllib.request.urlopen(video.thumbnail_url) as f:
                urllib.request.urlretrieve(
                    video.thumbnail_url, f"./videos/{video.author}/{title}/{title}.png")

        print(f"Downloaded: {video.title} successfully")

        process_audio(f"./videos/{video.author}/{title}/{title}.mp4")

    except Exception as e:
        logging.error(
            f"Error downloading {video.title} from {video.author}\n{url}\n{e}\n")


def process_audio(video_raw):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    print(f"[!] Processing audio {video_raw}")
    clip = VideoFileClip(video_raw)
    clip.audio.write_audiofile(f"{video_raw}.wav")

