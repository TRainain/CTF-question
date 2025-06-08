FROM python:3.8-alpine

LABEL Organization="qsnctf" Author="M0x1n <lqn@sierting.com>"

COPY files /tmp/

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.nju.edu.cn/g' /etc/apk/repositories \
    && apk update && apk add gcc build-base libffi-dev openssl-dev libev-dev \
    && pip install -U pip \
    && python -m pip install -U gunicorn[gevent,eventlet] \
    && mv /tmp/flag.sh /flag.sh \
    && mv /tmp/docker-entrypoint /usr/local/bin/docker-entrypoint \
    && chmod +x /usr/local/bin/docker-entrypoint

COPY app /app

EXPOSE 80

CMD ["/bin/sh", "-c", "docker-entrypoint"]