FROM continuumio/miniconda:4.1.11

USER root
RUN mkdir /opt/app

RUN useradd -ms /bin/bash crisprlab

USER root
RUN chown -R crisprlab /opt /home/crisprlab
RUN apt-get update --fix-missing && apt-get install -y less nano build-essential=11.7 rsync
#USER $CL_USER

RUN conda install -y -c bioconda -c biocore python=2.7 biopython=1.70 blast=2.6.0 minced=0.2.0 hmmer=3.1b2 pip=.1.2 conda=4.1.11

RUN pip install --upgrade pip
COPY . /opt/app
RUN cd /opt/app && pip install -e .

WORKDIR /home/crisprlab
#USER root

