"""A script to fulfill the database with images from "images/"""

import os

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for path in os.listdir("manual_tests/images"):
            url = "http://127.0.0.1:8000/image"
            files = {'image': open("manual_tests/images/" + path, 'rb')}
            requests.post(url, files=files)
            os.remove("manual_tests/images/" + path)
