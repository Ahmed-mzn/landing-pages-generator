# Generated by Django 4.1.4 on 2023-02-10 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_template_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='templates', to='main.domain'),
        ),
    ]
