# pyrefly: ignore [missing-import]
from rest_framework.routers import DefaultRouter
# pyrefly: ignore [missing-import]
from .views import ExpenseViewSet

routers=DefaultRouter()

routers.register('expenses', ExpenseViewSet, basename='expense')

urlpatterns=routers.urls