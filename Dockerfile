FROM python:3-alpine

RUN apk update && \
    apk add --no-cache pulseaudio pulseaudio-alsa alsa-plugins-pulse alsa-utils pulseaudio-utils ffmpeg sox && \
    pip3 install https://github.com/waggle-sensor/pywaggle/archive/v0.40.4.zip

COPY asound.conf /etc/asound.conf
COPY main.py .

# TODO scheduler should include this config and we should look at how to include into data discovery
ENV PULSE_SERVER=tcp:audio-server:4713

ENTRYPOINT [ "python3", "main.py" ]
