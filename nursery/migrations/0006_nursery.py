# Generated by Django 3.1.4 on 2021-01-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nursery', '0005_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nursery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
            ],
        ),
    ]