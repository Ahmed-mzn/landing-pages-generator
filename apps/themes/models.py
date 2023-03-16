from django.db import models


class ThemeCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'ThemeCategories'

    def __str__(self):
        return f'<Category {self.name}/>'


class Theme(models.Model):
    category = models.ForeignKey(ThemeCategory, related_name='themes', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    content = models.TextField()
    preview_content = models.TextField()
    image = models.FileField(upload_to='uploads/themes/%Y/%m/%d', null=True, blank=True)
    image_url = models.CharField(max_length=266, null=True, blank=True)
    only_admins = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Theme {self.name}/>'


class SectionCategory(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'SectionCategories'

    def __str__(self):
        return f'<Category {self.name}/>'


class Section(models.Model):
    category = models.ForeignKey(SectionCategory, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    content = models.TextField()
    image = models.FileField(upload_to='uploads/sections/%Y/%m/%d', null=True, blank=True)
    image_url = models.CharField(max_length=266, null=True, blank=True)
    only_admins = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Section {self.name}/>'
