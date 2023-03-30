"""webCode URL Configuration
"""
from django.urls import include, path
from rest_framework import routers
from IMDB.views import MovieViewSet

# Define Django Rest router
router = routers.DefaultRouter()
router.register(r'api/v1/movies', MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
