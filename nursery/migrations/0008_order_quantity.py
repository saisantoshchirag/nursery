# Generated by Django 3.1.4 on 2021-01-04 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery', '0007_plants_nursery'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
