#!/usr/bin/env python3
import argparse
import time
from waggle import plugin
from waggle.data.audio import Microphone
import logging


formats = ["ogg", "wav"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", default=formats[0], choices=formats, help="sample file format")
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
        filename = f"sample.{args.format}"
        sample.save(filename)
        plugin.upload_file(filename)


if __name__ == "__main__":
    main()
