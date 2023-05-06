from django.contrib import admin

from .models import Channel, ChannelField, ConstantChannel, ConstantChannelField, OrderItem, Order, Warehouse

admin.site.register(Channel)
admin.site.register(ChannelField)
admin.site.register(ConstantChannel)
admin.site.register(ConstantChannelField)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Warehouse)
