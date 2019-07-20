from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from image.models import get_image, save_images, get_closest_images
import json

from django.views.decorators.csrf import csrf_exempt  # for testing purposes

num_closest_images = 5

@csrf_exempt  # for testing purposes
def _get_closest(request, color):
    try:
        return HttpResponse(json.dumps(get_closest_images(color, num_closest_images)))
    except ValueError as e:
        return HttpResponse(content=e, status=500)


@csrf_exempt  # for testing purposes
def _get_image(request, id):
    try:
        return HttpResponse(get_image(id), content_type="image/jpeg")
    except KeyError as e:
        return HttpResponse(content=e, status=404)
    except FileNotFoundError as e:
        return HttpResponse(content=e, status=500)


@csrf_exempt  # for testing purposes
def _save_images(request):
    try:
        return HttpResponse(save_images(request.FILES))
    except ValidationError as e:
        return HttpResponse(content=e, status=500)
    except ValueError as e:
        return HttpResponse(content=e, status=415)
