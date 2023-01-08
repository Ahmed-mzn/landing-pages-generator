# Generated by Django 4.1.4 on 2022-12-30 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_domain_domain_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='domain',
        ),
        migrations.AddField(
            model_name='domain',
            name='app',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.app'),
            preserve_default=False,
        ),
    ]
