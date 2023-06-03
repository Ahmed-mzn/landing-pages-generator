from django.db import models
from apps.main.models import App, Template, Product, Lead, Affiliate, MainCity

from django.utils.translation import gettext_lazy as _

import uuid


class Channel(models.Model):
    CHANNEL_TYPE = (
        ('aymakan', 'Aymakan'),
        ('torod', 'Torod'),
        ('aramex', 'Aramex'),
        ('jonex', 'Jonex'),
        ('smsa', 'Smsa'),
    )

    app = models.ForeignKey(App, related_name='channels', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, choices=CHANNEL_TYPE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<CHANNEL {self.type}/>'


class ChannelField(models.Model):
    channel = models.ForeignKey(Channel, related_name="fields", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<FIELD {self.key} / {self.value}/>'


class ConstantChannel(models.Model):
    CHANNEL_TYPE = (
        ('aymakan', 'Aymakan'),
        ('torod', 'Torod'),
        ('aramex', 'Aramex'),
        ('jonex', 'Jonex'),
        ('smsa', 'Smsa'),
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, choices=CHANNEL_TYPE)
    image_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<CHANNEL_CONSTANT {self.type}/>'


class ConstantChannelField(models.Model):
    channel = models.ForeignKey(ConstantChannel, related_name="constant_fields", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<FIELD_CONSTANT {self.key} / {self.value}/>'


class Warehouse(models.Model):
    app = models.ForeignKey(App, related_name="warehouses", on_delete=models.CASCADE)
    city = models.ForeignKey(MainCity, related_name="warehouses", on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Warehouse {self.city}, {self.address} />"


class Coupon(models.Model):
    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
        ordering = ("-created_at",)

    COUPON_TYPE = (
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
    )

    app = models.ForeignKey(App, related_name="coupons", on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100, choices=COUPON_TYPE)
    percentage = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    num_available = models.IntegerField(default=0)
    num_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}"


class Order(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROGRESS = 'progress'
    INDELIVERY = 'indelivery'
    DELIVERED = 'delivered'
    # UNDELIVERED = 'undelivered'
    CANCELED = 'canceled'

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (CONFIRMED, 'confirmed'),
        (PROGRESS, 'progress'),
        (INDELIVERY, 'indelivery'),
        (DELIVERED, 'delivered'),
        # (UNDELIVERED, 'undelivered'),
        (CANCELED, 'canceled'),
    )

    COD = 'cod'
    CARD = 'card'

    PAYMENT_CHOICES = (
        (COD, 'cod'),
        (CARD, 'card'),
    )

    template = models.ForeignKey(Template, related_name='orders', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='orders', on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    affiliate = models.ForeignKey(Affiliate, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_company = models.ForeignKey(Channel, related_name='orders', on_delete=models.SET_NULL,
                                         null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_tracking_id = models.CharField(max_length=100, null=True, blank=True)
    shipping_awb = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=60, decimal_places=2)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, default=CARD)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lead.name} / {self.lead.city} / {self.template.template_code}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_orders', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=60, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} / {self.order.id}"
