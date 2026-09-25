from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from .views import GroupViewSet

routers=DefaultRouter()
routers.register('groups', GroupViewSet, basename='group')

urlpatterns=routers.urls