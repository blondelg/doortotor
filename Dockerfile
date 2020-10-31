# Staring image
FROM debian:latest
MAINTAINER geoffroy

# Install dependancies
RUN apt-get update && apt-get install -y \
	vim \
	git \
	wget\
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /home
RUN cd /home

# Download tor package

# Donlond tor signature

# Verify file integrity

