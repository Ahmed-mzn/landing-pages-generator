# Generated by Django 4.1.4 on 2023-05-01 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0004_affiliate_order_affiliate'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliate',
            name='full_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]