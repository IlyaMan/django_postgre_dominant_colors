from django.urls import path, re_path
from . import views

urlpatterns = [
    path("upload_image", views._save_image, name="upload_image"),
    path("get_image/<int:id>",
         views._get_image, name="get_image"),
    re_path("^get_closest/(?P<color>[0-9 A-F a-f]{6}$)",
            views._get_closest, name='get_closest')
]
