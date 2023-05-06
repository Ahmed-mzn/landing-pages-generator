from import_export import resources
from import_export.fields import Field

from apps.ship.models import Order


class OrderResource(resources.ModelResource):
    created_at = Field(attribute='created_at', column_name='التاريخ')
    quantity = Field(attribute='quantity', column_name='الكمية')
    product__title = Field(attribute='product__title', column_name='اسم المنتج')
    product__id = Field(attribute='product__id', column_name='معرف المنتج')
    lead__address = Field(attribute='lead__address', column_name='العنوان')
    lead__city = Field(attribute='lead__city', column_name='المدينة')
    lead__phone_number = Field(attribute='lead__phone_number', column_name='رقم الهاتف')
    lead__name = Field(attribute='lead__name', column_name='اسم الزبون')
    id = Field(attribute='lead__name', column_name='معرف الطلب')

    class Meta:
        model = Order
        fields = ('id', 'lead__name', 'lead__phone_number', 'lead__city', 'lead__address', 'product__id',
                  'product__title', 'quantity', 'created_at')
