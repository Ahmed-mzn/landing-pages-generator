# Generated by Django 4.1.4 on 2023-03-10 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_template_category_template_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='category',
            field=models.CharField(blank=True, max_length=85, null=True),
        ),
    ]
