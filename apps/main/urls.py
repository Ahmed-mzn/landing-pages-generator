from django.urls import path
from .views import TemplateLisView, AppLisView, AppByIdLisView, AppCreationListView

urlpatterns = [
    path('templates/', TemplateLisView.as_view(), name='templates'),
    path('apps/', AppLisView.as_view(), name='apps'),
    path('apps/create', AppCreationListView.as_view(), name='apps_create'),
    path('apps/<str:app_id>', AppByIdLisView.as_view(), name='app_by_id'),
]