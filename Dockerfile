FROM continuumio/miniconda:4.1.11

USER root
RUN mkdir /opt/app

RUN useradd -ms /bin/bash crisprlab

USER root
RUN chown -R crisprlab /opt /home/crisprlab
RUN apt-get update --fix-missing && apt-get install -y less nano rsync build-essential=11.7 pkg-config=0.28-1 python-matplotlib=1.4.2
#&& apt-get build-dep python-matplotlib=1.5.1
#USER $CL_USER

#requirements for binary tools called
RUN conda install -y -c bioconda -c biocore python=2.7 blast=2.6.0 minced=0.2.0 hmmer=3.1b2 pip=8.1.2 conda=4.1.11

#req for matlotlib in pip installable setup.py - see https://matplotlib.org/users/installing.html#installing-from-source
# tornado "cycler>=0.10" tk=8.6.7 libpng=1.6.34 zlib=1.2.11 freetype=2.

RUN pip install --upgrade pip
COPY . /opt/app
RUN cd /opt/app && pip install -e .

WORKDIR /home/crisprlab
#USER root

