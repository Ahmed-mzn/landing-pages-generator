# Generated by Django 4.1.4 on 2023-02-18 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_template_next_template_redirect_numbers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='total_redirect_numbers',
            field=models.IntegerField(default=10),
        ),
    ]