from django.urls import path
from .views import UserViewSet, SpotiApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user-viewset', UserViewSet, basename='user')

urlpatterns = [
    path('cancion/', SpotiApiView.as_view(), name='cancion-post'),
]   