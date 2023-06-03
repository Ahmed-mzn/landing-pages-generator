# Generated by Django 4.1.4 on 2023-06-02 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_template_card_payment_template_cod_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='screenshots/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='template',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d'),
        ),
    ]