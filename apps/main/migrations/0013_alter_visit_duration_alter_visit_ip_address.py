# Generated by Django 4.1.4 on 2023-01-02 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_visit_json_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='duration',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='visit',
            name='ip_address',
            field=models.CharField(max_length=30),
        ),
    ]
