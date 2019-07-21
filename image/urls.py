from django.urls import path, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    path("image", views.save_images, name="upload_image"),
    path("image/<uuid:id>",
         views.get_image, name="get_image"),
    re_path("^closest/(?P<color>[0-9 A-F a-f]{6}$)",
            views.get_closest, name='get_closest'),
    path('admin', admin.site.urls),
]
