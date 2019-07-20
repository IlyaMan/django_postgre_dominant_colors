from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import F, Model
import os.path
import logging

from lazysorted import LazySorted
import uuid

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
def get_closest_images(color, num):
    color = hex_to_rgb(color)

    def distance(v1):
        return (sum([(a - b)**2 for (a, b) in zip(v1, color)]))**(1 / 2)

    def key(x):
        return min(map(distance, x["colors"]))

    colors = Image.objects.all().values()
    return list(
        map(lambda x: x["id"], LazySorted(colors, key=key)[0:num])
    )


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


def get_image(id):
    try:
        image = Image.objects.all().get(id=id)
    except Image.DoesNotExist as e:
        raise KeyError("Wrong id")

    try:
        with open(image.path, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        logging.error(e)
        raise FileNotFoundError("File not found")


def save_images(images):
    for i in images.values():
        path = f"images/{uuid.uuid4().hex}.jpeg"
        with open(path, "wb") as f:
            f.write(i.read())
        colors = get_dominant_color(path)
        im = Image(colors=colors, path=path)
        im.save()
        return "Ok"


# Placeholder
def get_dominant_color(path="", num_clusters=3):
    try:
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    except cv2.error as e:
        raise ValueError("Invalid file: not an image")

    im = cv2.resize(im, (150, 150))
    ar = np.asarray(im, dtype=float)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])

    codes, _ = scipy.cluster.vq.kmeans(ar, num_clusters)
    vecs, _ = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = np.argpartition(counts, -3)[-3:]

    return [list(map(int, codes[i])) for i in index_max]
