<div align="center">
<h1 align="center">Customized Blogn and Authenticatiobn  (class-based and restframework)</h1>
<h3 align="center">Sample Project with base usage and deployment</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.django-rest-framework.org/" target="_blank"> <img src="https://img.icons8.com/?size=100&id=xeyzFtrzVyPM&format=png&color=000000" alt="rest-framework" width="40" height="40"/> </a>
<a href="https://redis.io/" target="_blank"> <img src="https://img.icons8.com/?size=100&id=FMw01QDk8Qlu&format=png&color=000000" alt="redis" width="40" height="40"/> </a>
<a href="https://docs.celeryq.dev/en/stable//" target="_blank"> <img src="https://docs.celeryq.dev/en/stable/_static/celery_512.png" alt="celery" width="40" height="40"/> </a>
<a href="https://gunicorn.org/" target="_blank"> <img src="https://gunicorn.org/images/logo.jpg" alt="gunicorn" width="40" height="40"/> </a>
<a href="https://nginx.org/en/" target="_blank"> <img src="https://nginx.org/nginx.png" alt="ngnix" width="40" height="40"/> </a>
<a href="https://locust.io/" target="_blank"> <img src="https://img.icons8.com/?size=100&id=3OYPTzNli067&format=png&color=000000" alt="locust" width="40" height="40"/> </a>
<a href="https://www.djangoproject.com/" target="_blank"> <img src="https://img.icons8.com/?size=100&id=qV-JzWYl9dzP&format=png&color=000000" alt="django" width="40" height="40"/> </a>



</p>




# Introduction
This project main goal is to show you how we can use django rest api to create a base blog app with customized authentications and all base needs.




# Features

 [Development usage](#development-usage)
  - [Clone the repo](#clone-the-repo)
  - [Enviroment Varibales](#enviroment-varibales)
  - [Build everything](#build-everything)
  - [Note](#note)
  - [Check it out in a browser](#check-it-out-in-a-browser)
- [Testing Usage](#testing-usage)
  - [running all tests](#running-all-tests)
- [CICD Deployment](#cicd-deployment)
  - [Github CICD](#github-cicd)
  
 
- [License](#license)
- [Bugs](#bugs)

# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. 

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.


## Clone the repo
Clone this repo anywhere you want and move into the directory:
```bash
git clone https://github.com/Ahmadzadeh920/Blog-Customized.git
```

## Enviroment Varibales
enviroment varibales are included in docker-compose.yml file for debugging mode and you are free to change commands inside:

```yaml
version: "3.9"
services:
  redis:
    container_name: redis
    image: redis
    restart: always
    ports:
      - "6379:6379"
    command: redis-server --save 60 1 --loglevel warning

  db:
      image: postgres:latest
      container_name: POSTGRES_DB
      environment:
        POSTGRES_DB: Customized-Blog-db
        POSTGRES_USER: admin_db
        POSTGRES_PASSWORD: as@123456
      volumes:
        - ./data/db:/var/lib/postgresql/data/

  backend:
      build: .
      container_name: backend
      command: python manage.py runserver 0.0.0.0:8000
      volumes:
        - ./core:/app
      ports:
        - "8000:8000"
      depends_on:
        - redis
        - db
    
  
  worker:
      build: .
      command: celery -A Core worker --loglevel=info
      volumes:
        - ./core:/app
      depends_on:
        - redis
        - backend
      

  smtp4dev:
      image: rnwood/smtp4dev:v3
      restart: always
      ports:
        # Change the number before : to the port the web interface should be accessible on
        - '5000:80'
        # Change the number before : to the port the SMTP server should be accessible on
        - '25:25'
        # Change the number before : to the port the IMAP server should be accessible on
        - '143:143'
      volumes:
        # This is where smtp4dev stores the database..
          - smtp4dev-data:/smtp4dev
      environment:
        - ServerOptions__HostName=smtp4dev


  master:
    image: locustio/locust
    ports:
     - "8089:8089"
    volumes:
      - ./core/locust:/mnt/locust
    command: -f /mnt/locust/locustfile.py --master -H http://backend:8000

  worker_locust:
    image: locustio/locust
    volumes:
      - ./core/locust:/mnt/locust
    command: -f /mnt/locust/locustfile.py --worker --master-host master


volumes:
  smtp4dev-data:



```

enviroment varibales are included in docker-compose-stage.yml file for deploying mode and you are free to change commands inside:

```yaml
version: "3.9"
services:
  redis:
    container_name: redis
    image: redis
    restart: always
    ports:
      - "6379:6379"
    command: redis-server --save 60 1 --loglevel warning
  

  

  backend:
    build: .
    container_name: backend
    
  
    volumes:
      - ./core:/app
      - static_volume:/app/static
      - media_volume:/app/media

    expose:
      - "8000"
    environment:
      - SECRET_KEY:${SECRET_KEY}
    depends_on:
      - redis
   
    command: gunicorn Core.wsgi --bind 0.0.0.0:8000
     #command: python manage.py runserver 0.0.0.0:8000
    networks:
      - default

  
  worker:
      build: .
      command: celery -A Core worker --loglevel=info
      volumes:
        - ./core:/app
      depends_on:
        - redis
        - backend
      




  nginx:
    image: nginx
    container_name: nginx
    restart: always
    ports: 
      - "80:80"
    volumes:
      - ./default.conf:/etc/nginx/conf.d/default.conf
      #app since in Dockerfile workdie is /app
      - static_volume:/home/app/static
      - media_volume:/home/app/media
    depends_on:
      - redis
      - backend

# this is introduced common volume
volumes:
  static_volume:
  media_volume:



networks:
  default:
    driver: bridge



```

## Build everything

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

```bash
docker-compose up --build
```
and for docker-compose-stage, you'll need to run the following:

```bash
docker-compose -f docker-compose-stage.yml  up --build
```

Now that everything is built and running we can treat it like any other Django
app.

## Note

If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.
## Check it out in a browser

Visit <http://localhost:8000> in your favorite browser.

# Testing Usage
## running all tests
```bash
docker compose run --rm backend sh -c " black -l 79 && flake8 && python manage.py test" -v core:/app
```
or
```bash
docker compose exec backend sh -c sh -c " black -l 79 && flake8 && python manage.py test" 
```
# CICD Deployment
For the sake of continuous integration and deployment i have provided two samples for github  for you.
but there will be some configurations to be added for building and deploying purposes.

## Github CICD
will be provided soon

# License
MIT.


# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.
