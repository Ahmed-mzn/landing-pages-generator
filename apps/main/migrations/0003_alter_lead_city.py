# Generated by Django 4.1.4 on 2023-05-12 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_affiliate_templateshare_affiliate_visit_affiliate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='main.city'),
        ),
    ]
