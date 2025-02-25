FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml /app/environment.yml

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "your_env_name", "/bin/bash", "-c"]

COPY . /app

EXPOSE 8000

RUN conda run -n your_env_name pip install uvicorn

CMD ["conda", "run", "-n", "ml_general", "python", "flood_nfip.py"]
