# Generated by Django 4.1.4 on 2023-02-21 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_templateshare_template_feature_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateshare',
            name='template',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='main.template'),
            preserve_default=False,
        ),
    ]
