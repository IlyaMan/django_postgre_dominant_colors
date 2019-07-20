from django.urls import path, re_path
from . import views

urlpatterns = [
    path("image", views._save_images, name="upload_image"),
    path("image/<uuid:id>",
         views._get_image, name="get_image"),
    re_path("^closest/(?P<color>[0-9 A-F a-f]{6}$)",
            views._get_closest, name='get_closest')
]
