FROM jupyter/datascience-notebook:387f29b6ca83

USER root

RUN addgroup nb_group \
    && usermod -aG nb_group jovyan
ENV CONDA_DIR /opt/conda
ENV SHELL /bin/bash
ENV PATH $CONDA_DIR/bin:$PATH

COPY fix-permissions /usr/local/bin/fix-permissions
RUN fix-permissions $CONDA_DIR
COPY . /opt/app
RUN fix-permissions /opt/app

#binary requirements
RUN apt-get update --fix-missing \
    && apt-get install -y build-essential=11.7 \ 
    && apt-get clean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

USER $NB_USER

RUN conda install -y -n python2 -c bioconda "python=2.7.12" "blast=2.6.0" "minced=0.2.0" "hmmer=3.1b2" \
    && conda clean -i -l -t -y \
    && rm -rf /tmp/* /var/tmp/*

#python requirements handled in setup.py
#need bash for conda
SHELL ["/bin/bash", "-c"]
RUN source activate python2 \
    && cd /opt/app \
    && pip install --disable-pip-version-check -e . \
    && rm -rf /$NB_USER/.cache/pip/*

