FROM python:3.8

# TODO see how much of this can be extracted out
RUN apt-get update && apt-get install -y --no-cache pulseaudio ffmpeg
COPY asound.conf /etc/asound.conf

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .

ENTRYPOINT [ "python3", "main.py" ]
