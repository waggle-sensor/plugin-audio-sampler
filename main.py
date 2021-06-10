#!/usr/bin/env python3
import argparse
import subprocess
import time
import waggle.plugin as plugin
import logging


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rate", default=300, type=float, help="sampling interval in seconds")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    plugin.init()

    logging.info("sampler started. will sample every %ss", args.rate)

    while True:
        time.sleep(args.rate)
        
        logging.info("recording raw audio sample")
        try:
            subprocess.check_call(["arecord", "-f", "cd", "-d", "30", "-r", "44100", "-c", "1", "sample.wav"])
        except subprocess.CalledProcessError:
            logging.info("failed to record wav. will retry")
            continue

        logging.info("converting sample to mp3")
        try:
            subprocess.check_call(["ffmpeg", "-y", "-i", "sample.wav", "-ac", "1", "-acodec", "mp3", "-ab", "128k", "sample.mp3"])
        except subprocess.CalledProcessError:
            logging.info("failed to convert to mp3. will retry")
            continue

        logging.info("uploading sample")
        plugin.upload_file("sample.mp3")


if __name__ == "__main__":
    main()
