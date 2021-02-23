#!/usr/bin/env python3
from datetime import datetime
import subprocess
import time
import waggle.plugin as plugin

def log(*args, **kwargs):
    print(*args, **kwargs, flush=True)

plugin.init()

while True:
    timestamp = datetime.now()
    
    log("recording raw audio sample")
    filename_wav = timestamp.strftime("/tmp/%Y-%m-%dT%H:%M:%S+00:00.wav")

    try:
        subprocess.check_call(["arecord", "-f", "cd", "-d", "3", "-r", "44100", "-c", "1", filename_wav])
    except subprocess.CalledProcessError:
        log("failed to record wav. will retry")
        time.sleep(10)
        continue

    log("uploading wav file")
    plugin.upload_file(filename_wav)

    log("encoding audio sample to mp3")
    filename_mp3 = filename_wav.replace(".wav", ".mp3")
    try:
        subprocess.run(["ffmpeg", "-i", filename_wav, "-ac", "1", "-acodec", "mp3", "-ab", "128k", filename_mp3])
    except subprocess.CalledProcessError:
        log("failed to encode mp3. will retry")
        time.sleep(10)
        continue

    log("uploading mp3 file")
    plugin.upload_file(filename_mp3)

    time.sleep(60)
