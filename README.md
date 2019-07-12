# Research project to explore Django and OpenCV

Server allows you to find five closest images to given color.
# Installation
## Prerequisites:
PostgreSQL listening on port 5432, with name and username "postgres" and password "docker". You can start a docker container like this:
`docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres`

## Setup:
```
pip3 install -r requirements.txt
cd manual_test_scripts/
python3 images_downloader.py
cd ..
python3 manage.py migrate```
run `python3 manage.py runserver` to start server
```cd manual_test_scripts/
python3 database_uploader.py
```

# Usage
Django server listens on port 8000 provides three endpoints:
- `get_closest/color`, which returns ids of five images closest to given color (e.g. `get_closest/FF00FF`)
- `upload_image`, which saves an image from multipart form
- `get_image/id`, which returns an image by id
