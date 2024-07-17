FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN rm -rf /root/.cache/pip
WORKDIR /app
COPY requirements.txt /Core/


RUN pip install -r requirements.txt


RUN pip install django==4.2
RUN pip install python-decouple
RUN pip install tzdata
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade djangorestframework
RUN pip install --upgrade markdown 
RUN pip install --upgrade django-filter
RUN pip install flake8
RUN pip install black
RUN pip install coreapi
RUN pip install Pillow
RUN pip install drf-yasg[validation]
RUN pip install django-allauth
RUN pip install django-allauth[socialaccount]
RUN pip install djangorestframework-simplejwt
RUN pip install -U django-jazzmin
RUN pip install -U django-mail-templated
RUN pip install PyJWT
RUN pip install djoser
RUN pip install pytest
RUN pip install pytest-django




COPY ./Core /app
