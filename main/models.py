from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import F, Model
import os.path

from lazysorted import LazySorted
import uuid
import json

import scipy
from scipy.cluster.vq import kmeans, vq
import numpy as np
import cv2


def validate_range(value):
    if not 0 <= value <= 255:
        raise ValidationError(
            (f'{value} is not in range [0, 255]')
        )


class Image(models.Model):
    colors = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(
                default=0, validators=[validate_range]),
            size=3),
        size=3
    )
    path = models.TextField(default="")

    def __str__(self):
        return f"{self.colors}"

    def save(self, *args, **kwargs):
        self.clean_fields()
        super(Image, self).save(*args, **kwargs)


# Placeholder
def get_closest(color, num):
    color = hex_to_rgb(color)
    if color is None:
        return None

    def distance(v1, v2):
        return (sum([(a - b)**2 for (a, b) in zip(v1, v2)]))**(1 / 2)

    def key(x):
        return min(map(lambda v: distance(v, color), x["colors"]))

    colors = Image.objects.all().values()
    return json.dumps(
        list(
            map(lambda x: x["id"], LazySorted(colors, key=key)[0:num])
        )
    )


def hex_to_rgb(hex):
    try:
        hex = str(hex)
        if len(hex) != 6:
            return None
        return [int(hex[0:2], 16),  # r
                int(hex[2:4], 16),  # g
                int(hex[4:6], 16)]  # b
    except ValueError:
        return None


def get_image(id):
    try:
        image = Image.objects.all().get(id=id)
    except Image.DoesNotExist:
        return None

    try:
        with open(image.path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


def upload_image(images):
    for i in images.values():
        path = f"images/{uuid.uuid4().hex}.jpeg"
        with open(path, "wb") as f:
            f.write(i.read())
        im = Image(colors=get_dominant_color(path), path=path)
        im.save()


# Placeholder
def get_dominant_color(path="", NUM_CLUSTERS=3):
    if not os.path.isfile(path):
        return None

    im = cv2.imread(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im = cv2.resize(im, (150, 150))
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
    codes, _ = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    vecs, _ = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = np.argpartition(counts, -3)[-3:]
    dominants = [list(map(int, codes[i])) for i in index_max]
    return dominants