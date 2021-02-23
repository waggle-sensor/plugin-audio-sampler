#!/usr/bin/env python3
from datetime import datetime
import subprocess
import time
import waggle.plugin as plugin

def log(*args, **kwargs):
    print(*args, **kwargs, flush=True)

plugin.init()

while True:
    log("recording raw audio sample")
    try:
        subprocess.check_call(["arecord", "-f", "cd", "-d", "3", "-r", "44100", "-c", "1", "sample.wav"])
    except subprocess.CalledProcessError:
        log("failed to record wav. will retry")
        time.sleep(10)
        continue

    log("uploading wav file")
    plugin.upload_file("sample.wav")

    time.sleep(60)
