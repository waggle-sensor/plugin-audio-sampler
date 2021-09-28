FROM python:3-alpine

# TODO see how much of this can be extracted out
RUN apk update && apk add --no-cache pulseaudio pulseaudio-alsa alsa-plugins-pulse
COPY asound.conf /etc/asound.conf

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .

ENTRYPOINT [ "python3", "main.py" ]
