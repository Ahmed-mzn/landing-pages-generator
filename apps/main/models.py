from django.db import models

from apps.authentication.models import User

import uuid


class Template(models.Model):
    name = models.CharField(max_length=85)
    path = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class App(models.Model):
    template = models.ForeignKey(Template, related_name='apps', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='apps', on_delete=models.CASCADE)
    app_id = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    domain = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    meta_keywords = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    main_image = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} app, template {self.template.name}"


class Product(models.Model):
    app = models.ForeignKey(App, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class FormsRecord(models.Model):
    app = models.ForeignKey(App, related_name='forms_records', on_delete=models.CASCADE)
    name = models.CharField(max_length=85)
    phone_number = models.CharField(max_length=85)
    city = models.CharField(max_length=85)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} / {self.city} / {self.app.app_id}"
