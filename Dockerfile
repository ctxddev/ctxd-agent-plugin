FROM python:3.12-slim@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159

RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir ctxd==0.1.16 \
    && useradd --create-home --uid 10001 ctxd \
    && mkdir /sources

COPY docker-entrypoint.sh /usr/local/bin/ctxd-container
RUN chmod 755 /usr/local/bin/ctxd-container

USER ctxd
WORKDIR /home/ctxd
ENTRYPOINT ["/usr/local/bin/ctxd-container"]
