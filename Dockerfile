# Staring image
FROM python:3.8
MAINTAINER geoffroy

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ports exposure
EXPOSE 8000
VOLUME /data

# Dependencies
RUN apt-get update && apt-get install -y \
	vim \
	git \
	tor \
	&& rm -rf /var/lib/apt/lists/*
