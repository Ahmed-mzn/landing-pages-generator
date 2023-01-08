from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('me/', views.UserDetailView.as_view(), name='me'),
]