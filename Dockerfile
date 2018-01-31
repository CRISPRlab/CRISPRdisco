FROM continuumio/miniconda:4.1.11

USER root

#binary requirements
RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends build-essential=11.7 \
  && apt-get clean && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN conda install -y -c bioconda "python=2.7.12" "blast=2.6.0" "minced=0.2.0" "hmmer=3.1b2" "conda=4.1.11" \
  && conda clean -i -l -t -y \
  && rm -rf /tmp/* /var/tmp/*

#python requirements handled in setup.py
COPY . /opt/app
RUN cd /opt/app && pip install --disable-pip-version-check -e . \
  && rm -rf /root/.cache/pip/* 

WORKDIR /home/crisprlab
ENTRYPOINT ["/usr/bin/tini", "--"]
