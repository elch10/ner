FROM continuumio/miniconda3

MAINTAINER Elchin "elchin1999@gmail.com"

RUN conda create -n env python=3 && conda init
RUN exec bash && conda activate env

RUN conda install -y -c anaconda flask
RUN conda install -y -c conda-forge pybind11==2.2.3 fasttext

# For deeppavlov
RUN conda install -y -c anaconda Cython==0.29.12 numpy==1.16.4 pandas==0.24.2 scipy==1.3.0 scikit-learn==0.21.2

RUN apt update && apt install -y build-essential
RUN pip install deeppavlov && \
    pip install git+https://github.com/deepmipt/bert.git@feat/multi_gpu

RUN pip install pullenti-wrapper

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]

