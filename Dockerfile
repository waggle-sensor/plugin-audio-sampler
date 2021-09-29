FROM python:3.8
RUN apt-get update && apt-get install --no-install-recommends -y pulseaudio && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY main.py .
COPY asound.conf /etc/asound.conf
ENTRYPOINT [ "python3", "main.py" ]
