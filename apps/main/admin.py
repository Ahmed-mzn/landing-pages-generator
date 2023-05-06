from django.contrib import admin

from .models import *


# admin.site.register(Template)
# admin.site.register(App)
# admin.site.register(Product)
# admin.site.register(FormsRecord)
# admin.site.register(Feature)
# admin.site.register(Review)


@admin.register(MainCity)
class MainCityAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en']
    list_filter = ['name_ar', 'name_en']


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['city', 'region', 'country']
    list_filter = ['city', 'region', 'country']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    list_filter = ['name', 'type']


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ['user', 'app_id']
    list_filter = ['user']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['app', 'template_code', 'description', 'meta_title']
    # ['meta_description', 'meta_keywords', 'logo', 'main_image', 'medals_image', 'second_image',
    # 'review_text', 'primary_color', 'secondary_color', 'created_at', 'updated_at']
    list_filter = ['app', 'template_code', 'meta_title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['app', 'title', 'description', 'price']
    list_filter = ['app', 'title', 'price']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['template', 'title', 'description']
    list_filter = ['title', 'template']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['template', 'username', 'comment', 'rating']
    list_filter = ['username', 'template']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'city']
    list_filter = ['city']


@admin.register(TemplateProduct)
class TemplateProductAdmin(admin.ModelAdmin):
    list_display = ['template', 'product']
    list_filter = ['product', 'template']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['app', 'main_city']
    list_filter = ['app', 'main_city']


@admin.register(TemplateShare)
class TemplateShareAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'template', 'city']
    list_filter = []
