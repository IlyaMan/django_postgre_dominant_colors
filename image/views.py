from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import ValidationError
from image.models import get_closest_images, Image, get_dominant_colors
import logging
import json

from django.views.decorators.csrf import csrf_exempt  # for testing purposes

num_closest_images = 5


def hex_to_rgb(hex):
    try:
        hex = str(hex)
        if len(hex) != 6:
            raise ValueError("Invalid color: incorrect length")
        return [int(hex[0:2], 16),  # r
                int(hex[2:4], 16),  # g
                int(hex[4:6], 16)]  # b
    except ValueError as e:
        raise ValueError("Invalid color: failed to parse as hex")


@csrf_exempt  # for testing purposes
@require_GET
def get_closest(request, color):
    try:
        rgb_color = hex_to_rgb(color)
        return HttpResponse(json.dumps(get_closest_images(rgb_color, num_closest_images)))
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
            # image_data = im.read_image_as_bytes()  # FIXME Under discussion
            # colors = get_dominant_colors(image_data)
            # im.save(colors)
            im.save()
        return HttpResponse()
    except ValidationError as e:
        return HttpResponse(content=e, status=500)
    except ValueError as e:
        return HttpResponse(content=e, status=415)
