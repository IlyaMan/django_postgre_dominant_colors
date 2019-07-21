from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import ValidationError
from image.models import get_closest_images, Image
import logging
import json

from django.views.decorators.csrf import csrf_exempt  # for testing purposes

num_closest_images = 5


@csrf_exempt  # for testing purposes
@require_GET
def get_closest(request, color):
    try:
        return HttpResponse(json.dumps(get_closest_images(color, num_closest_images)))
    except ValueError as e:
        return HttpResponse(content=e, status=500)


@csrf_exempt  # for testing purposes
@require_GET
def get_image(request, id):
    try:
        image = Image.objects.all().get(id=id)
        return HttpResponse(image.image, content_type="image/jpeg")
    except Image.DoesNotExist as e:
        return HttpResponse(content=KeyError("Wrong id"), status=404)
    except ValidationError as e:
        return HttpResponse(content=KeyError("Invalid id"), status=404)
    except FileNotFoundError as e:
        logging.error(e)
        return HttpResponse(content=FileNotFoundError("Image not found"), status=500)


@csrf_exempt  # for testing purposes
@require_POST
def save_images(request):
    try:
        for image in request.FILES.values():
            im = Image(image=image)
            im.save()
        return HttpResponse()
    except ValidationError as e:
        return HttpResponse(content=e, status=500)
    except ValueError as e:
        return HttpResponse(content=e, status=415)
