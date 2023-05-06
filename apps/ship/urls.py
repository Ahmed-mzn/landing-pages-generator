from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChannelAPI, get_constant_channels, test, OrderViewSet, CouponViewSet, AffiliateViewSet, \
    WarehouseViewSet

router = DefaultRouter()
router.register('channels', ChannelAPI, basename='channels')
router.register('orders', OrderViewSet, basename='orders')
router.register('coupons', CouponViewSet, basename='coupons')
router.register('affiliates', AffiliateViewSet, basename='affiliates')
router.register('warehouses', WarehouseViewSet, basename='warehouses')

urlpatterns = [
    path('', include(router.urls)),
    path('get_constant_channels', get_constant_channels, name='get_constant_channels'),
    path('test', test, name='test'),
    # path('create_app', AppCreationListView.as_view(), name='apps_create'),
]
