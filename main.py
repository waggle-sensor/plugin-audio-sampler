#!/usr/bin/env python3
import argparse
import time
from waggle import plugin
from waggle.data.audio import Microphone
import logging
import threading
import queue
import sys


def sampler_main(args, samples):
    mic = Microphone()    
    while True:
        time.sleep(args.rate)
        logging.info("recording audio sample")
        samples.put(mic.record(args.duration))


def main():
    parser = argparse.ArgumentParser()
    formats = ["flac", "ogg", "wav"]
    parser.add_argument("--format", default=formats[0], choices=formats, help="sample file format")
    parser.add_argument("--rate", default=300, type=float, help="sampling interval in seconds")
    parser.add_argument("--duration", default=30, type=float, help="sample duration in seconds")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S')

    plugin.init()

    logging.info("sampler started. will sample every %ss", args.rate)

    samples = queue.Queue()
    threading.Thread(target=sampler_main, args=(args, samples), daemon=True).start()

    timeout = 2*(args.rate + args.duration)

    while True:
        try:
            sample = samples.get(timeout=timeout)
        except Exception:
            logging.error("recording sample timed out")
            sys.exit(1)

        logging.info("saving and uploading sample")
        filename = f"sample.{args.format}"
        sample.save(filename)
        plugin.upload_file(filename, timestamp=sample.timestamp)


if __name__ == "__main__":
    main()
