FROM continuumio/miniconda:4.1.11

USER root
COPY start.sh /usr/local/bin

ENV CL_UID 1000
ENV CL_USER crisperlab
ENV CONDA_DIR /opt/conda
ENV SHELL /bin/bash
ENV PATH $CONDA_DIR/bin:$PATH


#binary requirements
RUN apt-get update --fix-missing && apt-get install -y build-essential=11.7 

RUN useradd -ms /bin/bash -N -u $CL_UID $CL_USER && \
    mkdir -p $CONDA_DIR && \
    chown $CL_USER $CONDA_DIR

USER $CL_USER
WORKDIR /home/crisprlab

RUN conda install -y -c bioconda "python=2.7*" "blast=2.6.0" "minced=0.2.0" "hmmer=3.1b2"

#python requirements handled in setup.py
RUN mkdir /opt/app
COPY . /opt/app
RUN cd /opt/app && pip install --disable-pip-version-check -e .

ENTRYPOINT ["/usr/local/bin/tini", "--", "start.sh"]


