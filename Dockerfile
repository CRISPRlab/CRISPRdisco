FROM continuumio/miniconda:4.1.11

USER root

ENV CL_UID 1000
ENV CL_USER crisperlab
ENV NB_USER $CL_USER
ENV CONDA_DIR /opt/conda
ENV SHELL /bin/bash
ENV PATH $CONDA_DIR/bin:$PATH

RUN useradd -ms /bin/bash -N -u $CL_UID $CL_USER
RUN addgroup nb_group \
    && usermod -aG nb_group $CL_USER
COPY start.sh /usr/local/bin/
COPY fix-permissions /usr/local/bin/
RUN fix-permissions $CONDA_DIR
COPY . /opt/app
RUN fix-permissions /opt/app

#binary requirements
RUN apt-get update --fix-missing && apt-get install -y build-essential=11.7

#RUN    mkdir -p $CONDA_DIR && \
#    chown -R $CL_USER $CONDA_DIR
#RUN mkdir -p /opt/app
#COPY . /opt/app
#RUN chown -R $CL_USER /opt/app

USER $CL_USER
RUN conda install -y -c bioconda "python=2.7*" "blast=2.6.0" "minced=0.2.0" "hmmer=3.1b2"

#python requirements handled in setup.py
RUN cd /opt/app && pip install --disable-pip-version-check -e .

WORKDIR /home/crisprlab
ENTRYPOINT ["/usr/bin/tini", "--", "start.sh"]
