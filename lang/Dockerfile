FROM debian:jessie
MAINTAINER James Kwan <jmkwan@ucsd.edu>

RUN apt-get update && apt-get install -y \
        python3-bitarray \
        python3-crypto \
        python3-pip \
        python3-ply
RUN pip3 install thriftpy

RUN apt-get clean

VOLUME ["/data"]

WORKDIR /data

CMD ["/data/launch-server.sh"]

EXPOSE 8000
