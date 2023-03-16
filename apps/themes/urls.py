from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('themes', ThemeView, basename='themes')
router.register('sections', SectionView, basename='sections')


urlpatterns = [
    path('', include(router.urls)),
]
