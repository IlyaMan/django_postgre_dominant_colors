"""A script to download some images from pexels.com"""

import requests
from bs4 import BeautifulSoup
import urllib.request
import uuid
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = set()
        searches = ["beautifull", "nature", "animals",
                    "pretty", "colors", "colorfull", "imagination"]

        for search in searches:
            page = requests.get("https://www.pexels.com/search/" + search)
            soup = BeautifulSoup(page.text, 'html.parser')
            for el in soup.find_all('img'):
                link = el.get('data-big-src', None)
                if link is not None:
                    res.add(link)

        print(len(res))
        for link in res:
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
            request = urllib.request.Request(link, None, hdr)
            resource = urllib.request.urlopen(request)
            output = open(f"manual_tests/images/{uuid.uuid4().hex}.jpeg", "wb")
            output.write(resource.read())
