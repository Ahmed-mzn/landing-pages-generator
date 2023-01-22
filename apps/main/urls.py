from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateViewSet, AppRetrieveDeleteUpdateView, AppByIdView, AppCreationListView, ProductViewSet, \
    FeatureViewSet, ReviewViewSet, check_domain, VisitAPIView, create_visit, create_form, FormAPIView, \
    get_template_one, get_template_two, get_app, get_template, AssignProductToTemplateView, UpdateDomainView, \
    create_blank_template

router = DefaultRouter()
router.register('templates', TemplateViewSet, basename='templates')
router.register('products', ProductViewSet, basename='products')
router.register('features', FeatureViewSet, basename='features')
router.register('reviews', ReviewViewSet, basename='reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('visits', VisitAPIView.as_view(), name='visits'),
    path('forms', FormAPIView.as_view(), name='forms'),
    path('apps/<str:app_id>', AppRetrieveDeleteUpdateView.as_view(), name='apps'),
    path('create_app', AppCreationListView.as_view(), name='apps_create'),
    path('templates/<int:template_id>/assign_product/<int:product_id>', AssignProductToTemplateView.as_view(),
         name='assign_product_to_template'),
    path('templates/create_blank_template', create_blank_template, name='create_blank_template'),
    path('domains/<int:pk>', UpdateDomainView.as_view(), name='update_domain'),
    path('get_app', get_app, name='get_app'),
    path('check_domain/<str:domain>', check_domain, name='check_domain'),

    # public api
    path('public/apps/<str:app_id>', AppByIdView.as_view(), name='app_by_id'),
    path('public/apps/template_one/<str:app_id>', get_template_one, name='get_template_one'),
    path('public/apps/template_two/<str:app_id>', get_template_two, name='get_template_two'),
    path('public/apps/templates/<str:template_id>', get_template, name='get_template'),
    path('public/create_visit', create_visit, name='create_visit'),
    path('public/create_form', create_form, name='create_form'),
]