# Generated by Django 4.1.4 on 2023-05-25 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_maincity_aramex'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='auto_ship_cc',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='app',
            name='auto_ship_cod',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='app',
            name='next_ship_channel',
            field=models.IntegerField(default=0),
        ),
    ]
