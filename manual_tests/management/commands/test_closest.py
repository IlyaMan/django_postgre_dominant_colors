"""A script to test "closest" endpoint from the main project"""

import requests
import cv2
import json
import urllib.request
import uuid
import os
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('color', nargs="+", type=str)

    def handle(self, *args, **options):
        for color in options["color"]:
            url = "http://127.0.0.1:8000/closest/" + color

            r = requests.get(url)
            if r.status_code != 200:
                print("Invalid color")
                exit()
            ids = json.loads(r.text)

            paths = []
            for i in ids:
                url = "http://127.0.0.1:8000/image/" + str(i)
                request = requests.get(url)
                path = f"manual_tests/temp/{uuid.uuid4().hex}.jpeg"
                output = open(path, "wb")
                output.write(request.content)
                paths.append(path)
                # OpenCV bug causes crashes here. Waiting for fix.
                # im = cv2.imread(path)
                # cv2.imshow(path, im)

            print("Images downloaded to temp/")
            input("press enter to clear temp")

            # OpenCV bug causes crashes here. Waiting for fix.
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            for path in paths:
                os.remove(path)
