# Generated by Django 4.1.4 on 2023-02-23 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_templateshare_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='label',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
