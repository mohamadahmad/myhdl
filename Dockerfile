# Dockerfile for yosys synthesis cosimulation test suite
#

FROM python:3.7-slim
RUN apt-get update --allow-releaseinfo-change ; \
	apt-get install -y wget gnupg iverilog graphviz

RUN wget -qO - https://section5.ch/section5-apt.key | apt-key add - 
RUN echo "deb http://section5.ch/debian buster non-free" > /etc/apt/sources.list.d/section5.list

RUN pip install --no-cache notebook

RUN apt-get update ; \
	apt-get install -y yosys-pyosys

ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
