FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        iperf3 \
        iputils-ping \
        curl \
        dnsutils \
        traceroute && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /netforge

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .
