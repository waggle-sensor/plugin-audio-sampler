#!/bin/sh

while true; do
    timestamp=$(date +%Y-%m-%dT%H:%M:%S+00:00)
    
    echo "recording raw audio sample"
    if ! arecord -f cd -d 3 -r 44100 -c 1 /tmp/$timestamp.wav; then
        echo "arecord failed. retrying..."
        sleep 3
        continue
    fi
    echo "created /tmp/$timestamp.wav"

    echo "encoding audio sample to mp3"
    if ! ffmpeg -i /tmp/$timestamp.wav -ac 1 -acodec mp3 -ab 128k /tmp/$timestamp.mp3; then
        echo "ffmpeg encoding failed. retrying..."
        sleep 3
        continue
    fi
    echo "created /tmp/$timestamp.mp3"

    echo "creating filtered audio sample"
    sox /tmp/$timestamp.wav -n noiseprof noise_profile_file
    sox /tmp/$timestamp.wav /tmp/output.wav noisered noise_profile_file 0.40
    sox /tmp/output.wav /tmp/bandpass.wav sinc 1.5k-0k
    sox -v 7 /tmp/bandpass.wav /tmp/$timestamp-filtered.mp3
    echo "created /tmp/$timestamp-filtered.mp3"

    # TODO add upload step

    sleep 60
done
