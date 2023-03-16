from .models import ThemeCategory, Theme, SectionCategory, Section
from rest_framework import serializers


class ThemeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeCategory
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    category = ThemeCategorySerializer(many=False)

    class Meta:
        model = Theme
        fields = ('id', 'category', 'content', 'name', 'image', 'image_url')


class SectionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionCategory
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    category = SectionCategorySerializer(many=False)

    class Meta:
        model = Section
        fields = ('id', 'category', 'content', 'name', 'image', 'image_url')
