FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
  build-essential \
  libmemcached-dev \
  python3-dev \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

COPY flag /flag
COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chown root:root /flag     && chmod 400 /flag
RUN chown root:root /readflag && chmod 4755 /readflag

COPY ./chall.py /app/
COPY ./requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN useradd --no-create-home --home-dir / --shell /bin/false kalmar

ENTRYPOINT ["uwsgi", "--http-socket", ":5000", "--plugin", "python", "--master", "--processes", "8", "--threads", "4", "--uid", "kalmar", "--gid", "kalmar", "--wsgi-file", "/app/chall.py"]
