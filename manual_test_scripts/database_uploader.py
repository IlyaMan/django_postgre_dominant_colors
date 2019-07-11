"""
A script to fulfill the database with images from "images/"
"""

import requests
import os

for path in os.listdir("images"):
    url = "http://127.0.0.1:8000/upload_image"
    files = {'image': open("images/" + path, 'rb')}
    r = requests.post(url, files=files)
