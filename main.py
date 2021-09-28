#!/usr/bin/env python3
import argparse
import time
from waggle import plugin
from waggle.data.audio import Microphone
import logging


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rate", default=300, type=float, help="sampling interval in seconds")
    parser.add_argument("--duration", default=30, type=float, help="sample duration in seconds")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    plugin.init()

    mic = Microphone()

    logging.info("sampler started. will sample every %ss", args.rate)

    while True:
        time.sleep(args.rate)
        
        logging.info("recording audio sample")
        sample = mic.record(args.duration)
        
        logging.info("uploading sample")
        sample.save("sample.mp3")
        plugin.upload_file("sample.mp3")


if __name__ == "__main__":
    main()
