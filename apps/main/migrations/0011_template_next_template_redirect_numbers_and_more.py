# Generated by Django 4.1.4 on 2023-02-18 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_formsrecord_amount_formsrecord_is_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='next_template_redirect_numbers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='template',
            name='template_redirect_numbers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='template',
            name='template_redirect_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
