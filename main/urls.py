from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from graphene_django.views import GraphQLView

urlpatterns = \
    [
        path('graphql', GraphQLView.as_view(graphiql=True)),
        path('', include('image.urls'))
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
