#FROM ubuntu:16.04
#changed to the below for access to CRISPRlab resources
FROM continuumio/miniconda

USER root
RUN mkdir /opt/app

RUN useradd -ms /bin/bash crisprlab

USER root
RUN chown -R crisprlab /opt /home/crisprlab
RUN apt-get update --fix-missing && apt-get install -y less nano build-essential rsync
#USER $CL_USER

RUN conda install -y -c bioconda -c biocore python=2.7 biopython blast minced hmmer pip conda

RUN pip install --upgrade pip
COPY . /opt/app
RUN cd /opt/app && pip install -e .

WORKDIR /home/crisprlab
#USER root

