#!/usr/bin/env python3
from datetime import datetime
import subprocess
import time
import waggle.plugin as plugin

def log(*args, **kwargs):
    print(*args, **kwargs, flush=True)

plugin.init()

log("sampler started. will sample every 5m")

while True:
    time.sleep(300)
    
    log("recording raw audio sample")
    try:
        subprocess.check_call(["arecord", "-f", "cd", "-d", "3", "-r", "44100", "-c", "1", "sample.wav"])
    except subprocess.CalledProcessError:
        log("failed to record wav. will retry")
        continue

    log("converting sample to mp3")
    try:
        subprocess.check_call(["ffmpeg", "-i", "sample.wav", "-ac", "1", "-acodec", "mp3", "-ab", "128k", "sample.mp3"])
    except subprocess.CalledProcessError:
        log("failed to convert to mp3. will retry")
        continue

    log("uploading sample")
    plugin.upload_file("sample.mp3")
