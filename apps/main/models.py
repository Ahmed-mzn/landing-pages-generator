from django.db import models

from apps.authentication.models import User

import uuid


class SofDelete(models.Model):
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class App(models.Model):
    user = models.ForeignKey(User, related_name='apps', on_delete=models.CASCADE)
    app_id = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    next_template = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} app, #{self.app_id}"


class Domain(models.Model):
    DOMAIN_TYPE = (
        ('custom', 'Custom'),
        ('normal', 'Normal')
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=22, choices=DOMAIN_TYPE)
    record_id = models.CharField(max_length=222, null=True, blank=True)
    app = models.OneToOneField(App, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Domain {self.name} / {self.type}>'


class Template(SofDelete):
    app = models.ForeignKey(App, related_name='templates', on_delete=models.CASCADE)
    template_code = models.CharField(max_length=85)
    template_name = models.CharField(max_length=85)
    description = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=200)
    logo = models.FileField(upload_to='uploads/%Y/%m/%d')
    main_image = models.FileField(upload_to='uploads/%Y/%m/%d')
    medals_image = models.FileField(upload_to='uploads/%Y/%m/%d')
    second_image = models.FileField(upload_to='uploads/%Y/%m/%d')
    review_text = models.CharField(max_length=200)
    primary_color = models.CharField(max_length=20)
    secondary_color = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_website = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Template {self.template_code} - {self.app.user}>"


class Product(SofDelete):
    app = models.ForeignKey(App, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.FileField(upload_to='uploads/%Y/%m/%d')
    price = models.FloatField()
    price_after_discount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Product {self.title}>"


class TemplateProduct(SofDelete):
    template = models.ForeignKey(Template, related_name='template_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_templates', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.template} / {self.product}"


class Feature(SofDelete):
    template = models.ForeignKey(Template, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Review(SofDelete):
    SCALE = (
        (1, '1/5'),
        (2, '2/5'),
        (3, '3/5'),
        (4, '4/5'),
        (5, '5/5'),
    )

    template = models.ForeignKey(Template, related_name='reviews', on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    comment = models.CharField(max_length=100)
    rating = models.IntegerField(choices=SCALE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} - {self.rating} stars'


class Visit(models.Model):
    template = models.ForeignKey(Template, related_name='visits', on_delete=models.CASCADE)
    city = models.CharField(max_length=85)
    region = models.CharField(max_length=85)
    country = models.CharField(max_length=85)
    location = models.CharField(max_length=222)
    ip_address = models.CharField(max_length=30)
    duration = models.CharField(max_length=100)
    json_object = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Visit {self.city}>"


class Lead(SofDelete):
    name = models.CharField(max_length=85)
    phone_number = models.CharField(max_length=85)
    city = models.CharField(max_length=85)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Lead {self.lead.name} / {self.lead.phone_number}>"


class FormsRecord(models.Model):
    template = models.ForeignKey(Template, related_name='forms_records', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='forms_templates', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='forms_leads', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lead.name} / {self.lead.city} / {self.template.template_code}"
