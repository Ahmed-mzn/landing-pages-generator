import os

from django.db import models
from django.core.files import File
from apps.authentication.models import User
from apps.themes.models import Theme

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from selenium import webdriver

import time
import uuid
import threading
import tempfile


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
    business_name = models.TextField(null=True, blank=True)
    next_template = models.IntegerField(default=0)
    auto_ship_cod = models.BooleanField(default=False)
    auto_ship_cc = models.BooleanField(default=True)
    next_ship_channel = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} app, #{self.app_id}"


class Domain(models.Model):
    DOMAIN_TYPE = (
        ('custom', 'Custom'),
        ('normal', 'Normal')
    )

    user = models.ForeignKey(User, related_name='domains', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=22, choices=DOMAIN_TYPE)
    record_id = models.CharField(max_length=222, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Domain {self.name} / {self.type}>'


class Template(SofDelete):
    app = models.ForeignKey(App, related_name='templates', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, related_name='templates', on_delete=models.SET_NULL, null=True, blank=True)
    theme = models.ForeignKey(Theme, related_name='templates', on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='child_templates', on_delete=models.SET_NULL, null=True, blank=True)
    is_child = models.BooleanField(default=False)
    next_template = models.IntegerField(default=0)
    next_template_redirect_numbers = models.IntegerField(default=0)
    total_redirect_numbers = models.IntegerField(default=10)
    template_redirect_numbers = models.IntegerField(default=0)
    template_redirect_percentage = models.IntegerField(default=0)
    template_code = models.CharField(max_length=85)
    template_name = models.CharField(max_length=85)
    category = models.CharField(max_length=85, null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    css = models.TextField(null=True, blank=True)
    js = models.TextField(null=True, blank=True)
    project_data = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    main_rating_title = models.CharField(max_length=50, null=True, blank=True)
    meta_description = models.CharField(max_length=200, null=True, blank=True)
    meta_keywords = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to='uploads/%Y/%m/%d', null=True, blank=True)
    preview_image = models.ImageField(upload_to='screenshots/%Y/%m/%d', null=True, blank=True)
    main_image = models.FileField(upload_to='uploads/%Y/%m/%d', null=True, blank=True)
    medals_image = models.FileField(upload_to='uploads/%Y/%m/%d', null=True, blank=True)
    second_image = models.FileField(upload_to='uploads/%Y/%m/%d', null=True, blank=True)
    review_text = models.CharField(max_length=200, null=True, blank=True)
    feature_text = models.CharField(max_length=200, null=True, blank=True)
    primary_color = models.CharField(max_length=20, null=True, blank=True)
    secondary_color = models.CharField(max_length=20, null=True, blank=True, default="#FBF4EA")
    extra_js = models.TextField(null=True, blank=True)
    cod_payment = models.BooleanField(default=True)
    card_payment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_website = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Template {self.template_code} - {self.template_name} / {self.app.user}>"

    def get_preview_image_url(self):
        if self.preview_image:
            return settings.WEBSITE_URL + self.preview_image.url
        return ''

    def make_screenshot(self):
        print("[+] Screenshot for template " + str(self.id) + " start")
        url = settings.WEBSITE_URL + f"/templates/preview-editor/{self.id}"

        drive_path = f"{settings.STATICFILES_DIRS[0]}/chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        options.add_argument("--hide-scrollbars")

        driver = webdriver.Chrome(executable_path=drive_path, options=options)
        driver.get(url)
        driver.set_window_size(1920, 1200)

        time.sleep(3)
        driver.save_screenshot(f'{settings.MEDIA_ROOT}/screenshots/screenshot-{self.id}.png')

        self.preview_image.save(f"screenshot-{self.id}.png",
                                File(open(f'{settings.MEDIA_ROOT}/screenshots/screenshot-{self.id}.png', 'rb')))
        print("[+] End screenshot for template " + str(self.id))

    class Meta:
        ordering = ('pk', )


class Product(SofDelete):
    app = models.ForeignKey(App, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    label = models.CharField(max_length=50, null=True, blank=True)
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
    description = models.TextField()
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
    comment = models.TextField()
    rating = models.IntegerField(choices=SCALE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} - {self.rating} stars'


class Affiliate(models.Model):
    app = models.ForeignKey(App, related_name='affiliates', on_delete=models.CASCADE)
    affiliate_identifier = models.CharField(max_length=200, default=uuid.uuid4)
    affiliate_secret = models.CharField(max_length=200, default=uuid.uuid4)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<AFFILIATE {self.email}/>'


class TemplateShare(models.Model):
    template = models.ForeignKey(Template, related_name='shares', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='shares', on_delete=models.CASCADE, null=True, blank=True)
    affiliate = models.ForeignKey(Affiliate, related_name='shares', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=85)
    city = models.CharField(max_length=85, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Visit(models.Model):
    template = models.ForeignKey(Template, related_name='visits', on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, related_name='visits', on_delete=models.SET_NULL, null=True, blank=True)
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


class MainCity(models.Model):
    name_ar = models.CharField(max_length=40)
    name_en = models.CharField(max_length=40)
    aymakan = models.CharField(max_length=40)
    aramex = models.CharField(max_length=40)
    jonex = models.CharField(max_length=40)
    smsa = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<MainCity {self.name_en}>"

    class Meta:
        verbose_name_plural = 'MainCities'


class City(models.Model):
    app = models.ForeignKey(App, related_name='cities', on_delete=models.CASCADE)
    main_city = models.ForeignKey(MainCity, related_name='main_cities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<City {self.main_city}>"

    class Meta:
        verbose_name_plural = 'Cities'


class Lead(SofDelete):
    name = models.CharField(max_length=85)
    phone_number = models.CharField(max_length=85)
    city = models.ForeignKey(City, related_name='leads', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Lead {self.name} / {self.phone_number}>"


# @receiver(post_save, sender=Template)
# def create_profile(sender, instance, created, **kwargs):
#     thread = threading.Thread(target=make_screenshot, args=(instance,))
#     thread.start()


# def make_screenshot(instance):
#     print("[+] Screenshot for template " + str(instance.id) + " start")
#     url = settings.WEBSITE_URL + f"/templates/preview-editor/{instance.id}"
#
#     drive_path = f"{settings.STATICFILES_DIRS[0]}/chromedriver.exe"
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     options.add_argument("--headless")
#     options.add_argument("--hide-scrollbars")
#
#     driver = webdriver.Chrome(executable_path=drive_path, options=options)
#     driver.get(url)
#     # driver.execute_script("document.body.style.overflow = 'hidden';")
#     driver.set_window_size(1920, 1200)
#
#     time.sleep(3)
#     driver.save_screenshot(f'{settings.MEDIA_ROOT}/screenshots/screenshot-{instance.id}.png')
#
#     # tmp = tempfile.NamedTemporaryFile(delete=False)
#     # driver.save_screenshot(tmp.name)
#     instance.preview_image.save(f"screenshots/screenshot-{instance.id}.png",
#                                 File(open(f'{settings.MEDIA_ROOT}/screenshots/screenshot-{instance.id}.png', 'rb')))
#     print("[+] End screenshot for template " + str(instance.id))
