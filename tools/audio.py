import os
import sys
from moviepy.editor import VideoFileClip
from vosk import Model, KaldiRecognizer


def process_audio(video):
    """Converts video to audio using MoviePy library
    that uses `ffmpeg` under the hood"""
    filename, ext = os.path.splitext(video)
    clip = VideoFileClip(video)
    clip.audio.write_audiofile(f"{filename}.wav")


#process_audio("I Got DRUNK & Turned Into FaZe WeenieWarrior420.mp4")



