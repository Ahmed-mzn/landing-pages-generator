# Generated by Django 4.1.4 on 2023-02-23 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_product_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='main_rating_title',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
