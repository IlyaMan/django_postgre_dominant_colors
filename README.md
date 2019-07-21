# Research project to explore Django and OpenCV

Server allows you to find five closest images to given color.
# Installation
## Prerequisites:
pipenv; python 3.7.4
PostgreSQL listening on port 5432, with name and username "postgres" and password "docker". You can start a docker container like this:
`docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres`

## Setup:
```
pipenv install
pipenv run python python manage.py migrate
pipenv run python manage.py download_images
```

run `python3 manage.py runserver` to start server

```
pipenv run python manage.py fulfill_database
```

Create a superuser if you want to acess Django Admin: `pipenv run python manage.py createsuperuser`

# Usage
Django server listens on port 8000 provides three endpoints:
- `closest/color`, which returns ids of five images closest to given color (e.g. `closest/FF00FF`) (`GET`)
- `image/id`, which returns an image by id (`GET`)
- `image`, which saves an image from multipart form (`POST`)
- `admin`, which gives an access to Django Admin (create a superuser to use it)