import graphene
from graphene_django.types import DjangoObjectType

from image.models import Image, get_closest_images
from image.views import hex_to_rgb, num_closest_images


class ImageType(DjangoObjectType):
    class Meta:
        model = Image


class Query(object):
    images = graphene.List(ImageType)

    image = graphene.Field(
        ImageType, id=graphene.UUID()
    )

    closest = graphene.List(graphene.String, color=graphene.String())

    def resolve_images(self, info, **kwargs):
        return Image.objects.all()

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Image.objects.all().get(id=id)
        return None

    def resolve_closest(self, info, **kwargs):
        color = kwargs.get('color')
        if color is not None:
            color = hex_to_rgb(color)
            return get_closest_images(color, num_closest_images)
        return None
