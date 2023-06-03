# Generated by Django 4.1.4 on 2023-05-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0011_order_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='type',
            field=models.CharField(choices=[('aymakan', 'Aymakan'), ('torod', 'Torod'), ('aramex', 'Aramex'), ('jonex', 'Jonex'), ('smsa', 'Smsa')], max_length=50),
        ),
        migrations.AlterField(
            model_name='constantchannel',
            name='type',
            field=models.CharField(choices=[('aymakan', 'Aymakan'), ('torod', 'Torod'), ('aramex', 'Aramex'), ('jonex', 'Jonex'), ('smsa', 'Smsa')], max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('confirmed', 'confirmed'), ('progress', 'progress'), ('indelivery', 'indelivery'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='pending', max_length=100),
        ),
    ]