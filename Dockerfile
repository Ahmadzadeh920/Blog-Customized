FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN rm -rf /root/.cache/pip
WORKDIR /app
COPY requirements.txt /Core/
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#RUN pip install -r requirements.txt
RUN pip install django==4.2
RUN pip install python-decouple
COPY ./Core /app
