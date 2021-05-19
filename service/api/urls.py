from django.urls import path
from api import views

urlpatterns = [
    path("", views.list_audio),
    path("gen_audio", views.gen_audio),
    path("get_audio/<path:uri>", views.get_audio),
    path("ocr", views.ocr)
]