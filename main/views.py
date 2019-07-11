from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from main.models import get_image, save_image, get_closest
import json

from django.views.decorators.csrf import csrf_exempt  # for testing purposes


@csrf_exempt  # for testing purposes
def _get_closest(request, color):
    try:
        return HttpResponse(json.dumps(get_closest(color, 5)))
    except ValueError as e:
        return HttpResponse(content=e, status=500)


@csrf_exempt  # for testing purposes
def _get_image(request, id):
    try:
        return HttpResponse(get_image(id), content_type="image/jpeg")
    except (KeyError, FileNotFoundError) as e:
        return HttpResponse(content=e, status=500)


@csrf_exempt  # for testing purposes
def _save_image(request):
    try:
        return HttpResponse(save_image(request.FILES))
    except (ValidationError, ValueError) as e:
        return HttpResponse(content=e, status=500)
