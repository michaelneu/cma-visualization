FROM jupyter/base-notebook

RUN mkdir /home/jovyan/notebooks
COPY jupyter_notebook_config.py /home/jovyan/.jupyter/

COPY --chown=1000:1000 cma /home/jovyan/cma
RUN mkdir -p $(python3 -m site --user-site) && mv ~/cma $(python3 -m site --user-site)
