FROM continuumio/miniconda3

MAINTAINER Elchin "elchin1999@gmail.com"

RUN apt-get update && apt-get install -y build-essential

RUN conda install -y -c anaconda flask Cython==0.29.12 numpy==1.16.4 pandas==0.24.2 scipy==1.3.0 scikit-learn==0.21.2
RUN conda install -y -c conda-forge pybind11==2.2.3 keras==2.2.4

RUN pip install deeppavlov
RUN python -m deeppavlov install ner_rus
RUN python -m deeppavlov download ner_rus
RUN pip install pullenti-wrapper
RUN pip install python-telegram-bot

COPY . /app
WORKDIR /app

# RUN python load_modules.py
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
