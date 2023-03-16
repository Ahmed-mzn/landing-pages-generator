from django.urls import path, include


from .simple_views import preview, preview_editor

urlpatterns = [
    # simple views
    path('templates/preview/<int:pk>', preview, name='preview'),
    path('templates/preview-editor/<int:pk>', preview_editor, name='preview2')
]
