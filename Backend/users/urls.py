from django.urls import path
# pyrefly: ignore [missing-import]
from .views import pingView

urlpatterns = [
    path("/ping",pingView, name="ping"),
]
