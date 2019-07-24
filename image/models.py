import uuid

import cv2
import numpy as np
import scipy
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from lazysorted import LazySorted
from scipy.cluster.vq import kmeans


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    colors = ArrayField(
        ArrayField(
            models.PositiveSmallIntegerField(
                validators=[MinValueValidator(0), MaxValueValidator(255)]),
            size=3),
        size=3,
        null=True,
        blank=True,
        default=None
    )
    image = models.ImageField(upload_to="", default="")

    def __str__(self):
        return self.image.name

    def read_image_as_bytes(self) -> np.ndarray:
        self.image.open("rb")  # FIXME Can't reopen closed files -> I don't close them
        image_bytes = self.image.read()
        # self.image.close() # FIXME
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            raise ValueError("Invalid file: not an image")
        return im


@receiver(pre_save, sender=Image)
def image_pre_save(sender, instance, **kwargs):
    # TODO test only, remove after
    instance.image.open()  # TEST
    print("File opened")
    instance.image.close()
    print("File closed")
    print("Attempt to reopen file")
    try:
        instance.image.open()
        print("Success")
    except ValueError as e:
        print("Failure:", e)  # TEST

    instance.read_image_as_bytes()  # Throws error if instance.image is not an image
    instance.clean_fields()


@receiver(post_save, sender=Image)
def image_post_save(sender, instance, **kwargs):
    if instance.colors is None:  # Prevent recursion
        im_bytes = instance.read_image_as_bytes()
        instance.colors = get_dominant_colors(im_bytes)
        instance.read_image_as_bytes()
        instance.clean_fields()
        instance.save()


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

    colors = Image.objects.all().exclude(colors__isnull=True).values()
    return list(
        map(lambda x: str(x["id"]), LazySorted(colors, key=key)[0:num])
    )
