FROM continuumio/miniconda:4.1.11

USER root
RUN mkdir /opt/app

#binary requirements
RUN apt-get update --fix-missing && apt-get install -y build-essential=11.7 
RUN conda install -y -c bioconda "python=2.7*" "blast=2.6.0" "minced=0.2.0" "hmmer=3.1b2"

#python requirements handled in setup.py
COPY . /opt/app
RUN cd /opt/app && pip install --disable-pip-version-check -e .

WORKDIR /home/crisprlab

