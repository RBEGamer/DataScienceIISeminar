FROM jupyter/datascience-notebook:latest

#RUN pip install --quiet --no-cache-dir -r ./requirements.txt && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"

WORKDIR /home/${NB_USER}
COPY ./jupyther_config/jupyter_notebook_config.py /home/${NB_USER}/.jupyter/jupyter_notebook_config.py
RUN conda install -y geopandas
RUN conda install -y matplotlib
RUN conda install -y geoplot
RUN conda install -y papermill
RUN conda install -y crontab

#RUN jupyter notebook --generate-config