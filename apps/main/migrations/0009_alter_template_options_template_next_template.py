# Generated by Django 4.1.4 on 2023-02-15 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_template_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'ordering': ('pk',)},
        ),
        migrations.AddField(
            model_name='template',
            name='next_template',
            field=models.IntegerField(default=0),
        ),
    ]
