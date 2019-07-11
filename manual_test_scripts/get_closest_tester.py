"""
A script to test "get_closest" endpoint from the main project
"""

import requests
import cv2
import json
import urllib.request
import uuid
import os
import sys

if __name__ == '__main__':
    color = sys.argv[1]
    url = "http://127.0.0.1:8000/get_closest/" + color

    r = requests.get(url)
    ids = json.loads(r.text)
    paths = []
    for i in ids:
        url = "http://127.0.0.1:8000/get_image/" + str(i)
        request = urllib.request.Request(url)
        resource = urllib.request.urlopen(request)
        path = f"temp/{uuid.uuid4().hex}.jpeg"
        output = open(path, "wb")
        output.write(resource.read())
        print(url)
        paths.append(path)
        im = cv2.imread(path)
        cv2.imshow(path, im)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for path in paths:
        os.remove(path)
