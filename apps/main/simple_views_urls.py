from django.urls import path, include


from .simple_views import preview

urlpatterns = [
    # simple views
    path('templates/preview/<int:pk>', preview, name='preview'),
]
