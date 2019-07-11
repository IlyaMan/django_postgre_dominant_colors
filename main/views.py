from django.shortcuts import render
from django.http import HttpResponse
from main.models import get_image, upload_image, get_closest
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # for testing purposes
def _get_closest(request, color):
    res = get_closest(color, 5)
    return HttpResponse(res)


@csrf_exempt  # for testing purposes
def _get_image(request, id):
    image = get_image(id)
    if image is not None:
        return HttpResponse(image, content_type="image/jpeg")
    else:
        return HttpResponse(None)


@csrf_exempt  # for testing purposes
def _upload_image(request):
    upload_image(request.FILES)
    return HttpResponse()
