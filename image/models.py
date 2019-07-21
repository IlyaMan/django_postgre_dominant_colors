from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from lazysorted import LazySorted
import uuid

import scipy
from scipy.cluster.vq import kmeans
import numpy as np
import cv2


def validate_range(value):
    if not 0 <= value <= 255:
        raise ValidationError(
            (f'{value} is not in range [0, 255]')
        )


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    colors = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(
                default=0, validators=[validate_range]),
            size=3),
        size=3
    )
    image = models.ImageField(upload_to="", default="")

    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        self.colors = self.get_dominant_colors(self.image.read())
        self.clean_fields()
        super(Image, self).save(*args, **kwargs)

    def get_dominant_colors(self, image_bytes, num_clusters=3):

        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
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


def get_closest_images(color, num):
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

    color = hex_to_rgb(color)

    def distance(v1):
        return (sum([(a - b) ** 2 for (a, b) in zip(v1, color)])) ** (1 / 2)

    def key(x):
        return min(map(distance, x["colors"]))

    colors = Image.objects.all().values()
    return list(
        map(lambda x: str(x["id"]), LazySorted(colors, key=key)[0:num])
    )
