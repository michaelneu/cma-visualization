FROM jupyter/base-notebook

RUN mkdir /home/jovyan/notebooks
COPY jupyter_notebook_config.py /home/jovyan/.jupyter/
