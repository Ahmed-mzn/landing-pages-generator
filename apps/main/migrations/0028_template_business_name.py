# Generated by Django 4.1.4 on 2023-03-23 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_alter_templateshare_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='business_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
