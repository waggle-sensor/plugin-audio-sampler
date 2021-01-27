FROM alpine:3.12.3

RUN apk update && \
    apk add --no-cache pulseaudio pulseaudio-alsa alsa-plugins-pulse alsa-utils pulseaudio-utils ffmpeg sox

COPY asound.conf /etc/asound.conf
COPY main.sh .

# TODO scheduler should include this config and we should look at how to include into data discovery
ENV PULSE_SERVER=tcp:audio-server:4713

ENTRYPOINT [ "sh", "main.sh" ]
