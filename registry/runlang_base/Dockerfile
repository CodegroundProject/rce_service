FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

# bla
ENV RUN_LANG_UBUNTU="18.04"
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN apt-get install -y python3.7 python3-pip
