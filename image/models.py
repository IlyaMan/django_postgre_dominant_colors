from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.postgres.fields import ArrayField

from lazysorted import LazySorted
import uuid

import scipy
from scipy.cluster.vq import kmeans
import numpy as np
import cv2


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    colors = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(
                default=0, validators=[MinValueValidator(0), MaxValueValidator(255)]),
            size=3),
        size=3
    )
    image = models.ImageField(upload_to="", default="")

    def __str__(self):
        return self.image.name

    def read_image_as_bytes(self) -> np.ndarray:
        image_bytes = self.image.read()
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            raise ValueError("Invalid file: not an image")
        return im

    def save(self, *args, **kwargs):
        self.colors = get_dominant_colors(self.read_image_as_bytes())  # FIXME Under discussion
        self.clean_fields()
        super(Image, self).save(*args, **kwargs)


def get_dominant_colors(im: np.ndarray, num_clusters=3):
    im = cv2.resize(im, (150, 150))
    ar = np.asarray(im, dtype=float)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])

    codes, _ = scipy.cluster.vq.kmeans(ar, num_clusters)
    vecs, _ = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = np.argpartition(counts, -3)[-3:]

    return [list(map(int, codes[i])) for i in index_max]


def get_closest_images(rgb_color, num) -> list:
    def distance(v1):
        return (sum([(a - b) ** 2 for (a, b) in zip(v1, rgb_color)])) ** (1 / 2)

    def key(x):
        return min(map(distance, x["colors"]))

    colors = Image.objects.all().values()
    return list(
        map(lambda x: str(x["id"]), LazySorted(colors, key=key)[0:num])
    )
