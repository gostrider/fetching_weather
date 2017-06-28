FROM ubuntu:14.04

WORKDIR /usr/src

RUN apt-get update --yes && apt-get upgrade --yes \
    && apt-get install git wget build-essential checkinstall --yes \
    && apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev --yes \
    && wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz \
    && wget http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-2-amd64.deb \
    && tar zxf Python-3.6.0.tgz \
    && cd Python-3.6.0 \
    && ./configure && make altinstall \
    && easy_install-3.6 pip \
    && cd /usr/src \
    && dpkg -i couchbase-release-1.0-2-amd64.deb \
    && apt-get update --yes \
    && apt-get install libcouchbase-dev libcouchbase2-bin build-essential --yes \
    && pip install couchbase tornado \
    && git clone https://github.com/gostrider/fetching_weather.git

RUN cd fetching_weather

ENTRYPOINT exec /usr/local/bin/python3.6 /usr/src/fetching_weather/main.py
