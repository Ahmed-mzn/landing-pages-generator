from django.contrib import admin

from .models import *


admin.site.register(ThemeCategory)
admin.site.register(SectionCategory)


@admin.register(Theme)
class ThemeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']


@admin.register(Section)
class ThemeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']