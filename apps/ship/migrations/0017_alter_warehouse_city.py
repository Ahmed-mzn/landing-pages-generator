# Generated by Django 4.1.4 on 2023-06-03 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_affiliate_is_deleted_city_is_deleted'),
        ('ship', '0016_coupon_is_deleted_warehouse_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='main.maincity'),
            preserve_default=False,
        ),
    ]